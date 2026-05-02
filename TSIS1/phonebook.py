import csv
import json
from datetime import datetime
from connect import get_connection


def get_group_id(group_name):
    """Возвращает id группы, если группы нет – создаёт."""
    conn, cur = get_connection()
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()
    if row:
        group_id = row[0]
    else:
        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
        group_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return group_id


def insert_from_csv(file_path):
    """Расширенный импорт из CSV (поддерживает email, birthday, group, доп. телефоны)"""
    conn, cur = get_connection()
    with open(file_path, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            cur.execute("SELECT id FROM contacts WHERE name = %s", (row["name"],))
            if cur.fetchone():
                overwrite = input(f"Контакт '{row['name']}' уже существует. Перезаписать? (y/n): ").strip().lower()
                if overwrite != 'y':
                    continue
                
                cur.execute("DELETE FROM contacts WHERE name = %s", (row["name"],))
            
            
            group_id = None
            if row.get("group"):
                group_id = get_group_id(row["group"])
            
            
            cur.execute(
                """INSERT INTO contacts (name, phone, email, birthday, group_id)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (row["name"], row.get("phone", ""), row.get("email"), row.get("birthday"), group_id)
            )
            contact_id = cur.fetchone()[0]
            
            
            if row.get("additional_phone") and row.get("phone_type"):
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, row["additional_phone"], row["phone_type"])
                )
    conn.commit()
    cur.close()
    conn.close()
    print("CSV импорт завершён.")

def insert_from_console():
    """Добавление контакта вручную с новыми полями"""
    name = input("Имя: ")
    phone = input("Основной телефон: ")
    email = input("Email (необязательно): ") or None
    birthday = input("Дата рождения (ГГГГ-ММ-ДД, необязательно): ") or None
    
    
    conn, cur = get_connection()
    cur.execute("SELECT name FROM groups ORDER BY name")
    groups = cur.fetchall()
    print("Доступные группы:")
    for i, g in enumerate(groups, 1):
        print(f"{i}. {g[0]}")
    print("0. Без группы")
    choice = input("Выберите группу: ")
    group_id = None
    if choice != '0' and choice.isdigit():
        group_name = groups[int(choice)-1][0]
        group_id = get_group_id(group_name)
    
    cur.execute(
        "INSERT INTO contacts (name, phone, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (name, phone, email, birthday, group_id)
    )
    contact_id = cur.fetchone()[0]
    
    
    while True:
        add = input("Добавить ещё телефон? (y/n): ").strip().lower()
        if add != 'y':
            break
        extra_phone = input("Номер: ")
        ptype = input("Тип (home/work/mobile): ").strip().lower()
        if ptype in ('home','work','mobile'):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact_id, extra_phone, ptype))
        else:
            print("Неверный тип, пропускаем.")
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен.")

def update_contact():
    """Обновление с возможностью менять email, birthday, группу"""
    conn, cur = get_connection()
    name = input("Введите имя контакта для обновления: ")
    
    cur.execute("SELECT id, name, phone, email, birthday, group_id FROM contacts WHERE name ILIKE %s", (f"%{name}%",))
    contacts = cur.fetchall()
    if not contacts:
        print("Контакты не найдены.")
        cur.close()
        conn.close()
        return
    if len(contacts) > 1:
        print("Найдено несколько:")
        for i, c in enumerate(contacts, 1):
            print(f"{i}. {c[1]} - {c[2]}")
        idx = int(input("Выберите номер: ")) - 1
        contact = contacts[idx]
    else:
        contact = contacts[0]
    contact_id, old_name, old_phone, old_email, old_bday, old_group_id = contact
    
    print("1. Имя\n2. Телефон\n3. Email\n4. День рождения\n5. Группу")
    field = input("Что обновить? ")
    if field == "1":
        new_name = input("Новое имя: ")
        cur.execute("UPDATE contacts SET name=%s WHERE id=%s", (new_name, contact_id))
    elif field == "2":
        new_phone = input("Новый основной телефон: ")
        cur.execute("UPDATE contacts SET phone=%s WHERE id=%s", (new_phone, contact_id))
    elif field == "3":
        new_email = input("Новый email: ") or None
        cur.execute("UPDATE contacts SET email=%s WHERE id=%s", (new_email, contact_id))
    elif field == "4":
        new_bday = input("Новая дата (ГГГГ-ММ-ДД): ") or None
        cur.execute("UPDATE contacts SET birthday=%s WHERE id=%s", (new_bday, contact_id))
    elif field == "5":
       
        cur.execute("SELECT name FROM groups")
        groups = [row[0] for row in cur.fetchall()]
        print("Группы:", ", ".join(groups))
        new_group = input("Введите название группы: ")
        gid = get_group_id(new_group)
        cur.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (gid, contact_id))
    else:
        print("Неверный выбор")
    conn.commit()
    cur.close()
    conn.close()
    print("Обновлено.")

def search_contacts():
    """Расширенный поиск через хранимую функцию search_contacts"""
    query = input("Введите текст для поиска (имя, email, телефон): ").strip()
    if not query:
        return
    conn, cur = get_connection()
    cur.callproc("search_contacts", (query,))
    rows = cur.fetchall()
    if not rows:
        print("Ничего не найдено.")
    else:
        for row in rows:
            print(f"Имя: {row[0]}, Тел: {row[1]}, Email: {row[2]}, ДР: {row[3]}, Группа: {row[4]}, Доп.телефоны: {row[5]}")
    cur.close()
    conn.close()

def delete_contact():
    """Удаление контакта по имени или телефону (работает с каскадным удалением телефонов)"""
    conn, cur = get_connection()
    choice = input("Удалить по: 1) Имя 2) Телефон: ")
    if choice == "1":
        name = input("Имя: ")
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    elif choice == "2":
        phone = input("Телефон: ")
        
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
    else:
        print("Неверно")
        return
    conn.commit()
    cur.close()
    conn.close()
    print("Удаление выполнено.")


def manage_phones():
   
    name = input("Введите имя контакта: ")
    conn, cur = get_connection()
    cur.execute("SELECT id, name FROM contacts WHERE name ILIKE %s", (f"%{name}%",))
    contacts = cur.fetchall()
    if not contacts:
        print("Не найдено.")
        cur.close()
        conn.close()
        return
    if len(contacts) > 1:
        for i, c in enumerate(contacts, 1):
            print(f"{i}. {c[1]}")
        idx = int(input("Выберите: ")) - 1
        contact_id = contacts[idx][0]
    else:
        contact_id = contacts[0][0]
    
    while True:
        cur.execute("SELECT id, phone, type FROM phones WHERE contact_id=%s", (contact_id,))
        phones = cur.fetchall()
        print("\nДополнительные телефоны:")
        for p in phones:
            print(f"{p[0]}: {p[1]} ({p[2]})")
        print("1. Добавить телефон")
        print("2. Удалить телефон")
        print("3. Назад")
        opt = input("Выбор: ")
        if opt == "1":
            phone = input("Номер: ")
            ptype = input("Тип (home/work/mobile): ").strip().lower()
            if ptype in ('home','work','mobile'):
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                            (contact_id, phone, ptype))
                conn.commit()
                print("Добавлен.")
            else:
                print("Неверный тип.")
        elif opt == "2":
            pid = input("ID телефона для удаления: ")
            cur.execute("DELETE FROM phones WHERE id=%s AND contact_id=%s", (pid, contact_id))
            conn.commit()
            print("Удалён, если существовал.")
        elif opt == "3":
            break
    cur.close()
    conn.close()

def move_to_group():
    """Перемещение контакта в другую группу (вызов процедуры)"""
    name = input("Имя контакта: ")
    group = input("Название группы: ")
    conn, cur = get_connection()
    try:
        cur.callproc("move_to_group", (name, group))
        conn.commit()
        print(f"Контакт '{name}' перемещён в группу '{group}'")
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def export_to_json():
    """Экспорт всех контактов в JSON"""
    filename = input("Имя файла для экспорта (например, contacts.json): ").strip()
    conn, cur = get_connection()
    query = """
        SELECT 
            c.name, c.phone, c.email, c.birthday, g.name as group_name,
            json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.phone, c.email, c.birthday, g.name
        ORDER BY c.name
    """
    cur.execute(query)
    rows = cur.fetchall()
    data = []
    for row in rows:
        contact = {
            "name": row[0],
            "primary_phone": row[1],
            "email": row[2],
            "birthday": str(row[3]) if row[3] else None,
            "group": row[4],
            "additional_phones": row[5] if row[5] else []
        }
        data.append(contact)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Экспортировано {len(data)} контактов в {filename}")
    cur.close()
    conn.close()

def import_from_json():
    """Импорт из JSON с обработкой дубликатов (skip/overwrite)"""
    filename = input("Имя JSON файла: ").strip()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            contacts = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения: {e}")
        return
    
    conn, cur = get_connection()
    for contact in contacts:
        name = contact["name"]
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exists = cur.fetchone()
        if exists:
            action = input(f"Контакт '{name}' существует. Пропустить (s) или перезаписать (o)? ").strip().lower()
            if action == 's':
                continue
            elif action == 'o':
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            else:
                print("Неверный ввод, пропускаем")
                continue
        # Вставка
        group_id = None
        if contact.get("group"):
            group_id = get_group_id(contact["group"])
        cur.execute(
            "INSERT INTO contacts (name, phone, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (name, contact.get("primary_phone", ""), contact.get("email"), contact.get("birthday"), group_id)
        )
        contact_id = cur.fetchone()[0]
        for phone_data in contact.get("additional_phones", []):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact_id, phone_data["phone"], phone_data["type"]))
    conn.commit()
    cur.close()
    conn.close()
    print("Импорт завершён.")


current_page = 0
page_size = 10
current_sort = "name"
current_group_filter = None
current_search = None

def get_filtered_contacts():
    """Возвращает список контактов с учётом фильтра, сортировки и пагинации"""
    conn, cur = get_connection()
    query = """
        SELECT 
            c.name, c.phone, c.email, c.birthday, g.name as group_name,
            STRING_AGG(DISTINCT p.phone || ' (' || p.type || ')', ', ') as extra_phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE 1=1
    """
    params = []
    if current_group_filter:
        query += " AND g.name = %s"
        params.append(current_group_filter)
    if current_search:
        query += " AND (c.name ILIKE %s OR c.email ILIKE %s OR c.phone ILIKE %s OR p.phone ILIKE %s)"
        search_pattern = f"%{current_search}%"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
    query += " GROUP BY c.id, c.name, c.phone, c.email, c.birthday, g.name"
    
    # Сортировка
    if current_sort == "name":
        query += " ORDER BY c.name"
    elif current_sort == "birthday":
        query += " ORDER BY c.birthday NULLS LAST"
    elif current_sort == "date_added":
        query += " ORDER BY c.created_at"
    
    query += " LIMIT %s OFFSET %s"
    params.extend([page_size, current_page * page_size])
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_total_count():
    """Общее количество контактов с учётом фильтров"""
    conn, cur = get_connection()
    query = "SELECT COUNT(DISTINCT c.id) FROM contacts c LEFT JOIN groups g ON c.group_id=g.id LEFT JOIN phones p ON c.id=p.contact_id WHERE 1=1"
    params = []
    if current_group_filter:
        query += " AND g.name = %s"
        params.append(current_group_filter)
    if current_search:
        query += " AND (c.name ILIKE %s OR c.email ILIKE %s OR c.phone ILIKE %s OR p.phone ILIKE %s)"
        sp = f"%{current_search}%"
        params.extend([sp, sp, sp, sp])
    cur.execute(query, params)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def view_contacts_paginated():
    """Показать контакты с пагинацией, фильтром и сортировкой"""
    total = get_total_count()
    if total == 0:
        print("Нет контактов.")
        return
    total_pages = (total + page_size - 1) // page_size
    contacts = get_filtered_contacts()
    print(f"\n=== Страница {current_page+1} из {total_pages} ===")
    print(f"Фильтр по группе: {current_group_filter or 'Все'}")
    print(f"Сортировка: {current_sort}")
    print(f"Поиск: {current_search or 'Нет'}\n")
    for c in contacts:
        print(f"Имя: {c[0]}")
        print(f"  Тел: {c[1]}, Email: {c[2]}, ДР: {c[3]}, Группа: {c[4]}")
        if c[5]:
            print(f"  Доп. телефоны: {c[5]}")
        print("-"*40)

def filter_by_group():
    """Интерактивная фильтрация по группе"""
    global current_group_filter, current_page
    conn, cur = get_connection()
    cur.execute("SELECT name FROM groups ORDER BY name")
    groups = cur.fetchall()
    cur.close()
    conn.close()
    print("0. Сбросить фильтр")
    for i, g in enumerate(groups, 1):
        print(f"{i}. {g[0]}")
    choice = input("Выберите группу: ")
    if choice == "0":
        current_group_filter = None
    elif choice.isdigit() and 1 <= int(choice) <= len(groups):
        current_group_filter = groups[int(choice)-1][0]
    current_page = 0
    view_contacts_paginated()

def change_sort():
    """Смена сортировки"""
    global current_sort, current_page
    print("1. По имени")
    print("2. По дню рождения")
    print("3. По дате добавления")
    choice = input("Выберите: ")
    if choice == "1":
        current_sort = "name"
    elif choice == "2":
        current_sort = "birthday"
    elif choice == "3":
        current_sort = "date_added"
    else:
        print("Неверно, оставляем как есть")
    current_page = 0
    view_contacts_paginated()

def search_and_filter():
    """Установка поискового запроса"""
    global current_search, current_page
    query = input("Введите текст для поиска (или Enter для сброса): ").strip()
    current_search = query if query else None
    current_page = 0
    view_contacts_paginated()

def pagination_navigation():
    """Навигация по страницам"""
    global current_page
    total = get_total_count()
    if total == 0:
        print("Нет данных.")
        return
    total_pages = (total + page_size - 1) // page_size
    while True:
        print(f"\nСтраница {current_page+1} / {total_pages}")
        print("n - следующая, p - предыдущая, g - перейти, q - выход")
        cmd = input("> ").strip().lower()
        if cmd == 'n' and current_page+1 < total_pages:
            current_page += 1
            view_contacts_paginated()
        elif cmd == 'p' and current_page > 0:
            current_page -= 1
            view_contacts_paginated()
        elif cmd == 'g':
            try:
                p = int(input("Номер страницы: ")) - 1
                if 0 <= p < total_pages:
                    current_page = p
                    view_contacts_paginated()
                else:
                    print("Неверный номер")
            except:
                print("Ошибка")
        elif cmd == 'q':
            break
        else:
            print("Недопустимая команда")

def main():
    global current_page, current_sort, current_group_filter, current_search
    while True:
        print("\n=== РАСШИРЕННЫЙ ТЕЛЕФОННЫЙ СПРАВОЧНИК ===")
        print("1. Показать контакты (с фильтром/сортировкой)")
        print("2. Добавить контакт вручную")
        print("3. Импорт из CSV")
        print("4. Обновить контакт")
        print("5. Поиск (расширенный)")
        print("6. Удалить контакт")
        print("7. Управление дополнительными телефонами")
        print("8. Переместить в группу")
        print("9. Экспорт в JSON")
        print("10. Импорт из JSON")
        print("11. Фильтр по группе")
        print("12. Сменить сортировку")
        print("13. Поиск/фильтр (по тексту)")
        print("14. Пагинация (вперёд/назад)")
        print("0. Выход")
        choice = input("Выбор: ")
        
        if choice == "1":
            view_contacts_paginated()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv("contacts.csv")  
        elif choice == "4":
            update_contact()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            manage_phones()
        elif choice == "8":
            move_to_group()
        elif choice == "9":
            export_to_json()
        elif choice == "10":
            import_from_json()
        elif choice == "11":
            filter_by_group()
        elif choice == "12":
            change_sort()
        elif choice == "13":
            search_and_filter()
        elif choice == "14":
            pagination_navigation()
        elif choice == "0":
            break
        else:
            print("Неверный пункт")

if __name__ == "__main__":
    main()
