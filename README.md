# Watches-Shop

Bu veb-sayt **soat sotuvchi do'kon** uchun yaratilgan. Veb-sayt **Django** frameworkida qurilgan va **SQLite3** ma'lumotlar bazasidan foydalanadi. Veb-saytning asosiy maqsadi - mijozlarga soatlarni ko'rish, tanlash va xarid qilish imkoniyatini berish.

## Veb-saytning imkoniyatlari

- **Soatlarni ko'rish**:
  - Barcha mavjud soatlarni kategoriyalar bo'yicha ko'rish.
- **Soat haqida to'liq ma'lumot**:
  - Har bir soat haqida batafsil ma'lumot (narxi, brendi, tavsifi va boshqalar).
- **Xarid qilish**:
  - Mijozlar soatlarni savatga qo'shishi va xarid qilishi mumkin.
- **Admin panel**:
  - Do'kon egasi yangi soatlar qo'shishi, mavjud soatlarni tahrirlashi yoki o'chirishi mumkin.

## Texnologiyalar

- **Django** - Python dasturlash tili uchun kuchli veb-framework.
- **SQLite3** - Yengil va samarali ma'lumotlar bazasi.
- **HTML/CSS/JavaScript** - Veb-saytning frontend qismi.
- **Bootstrap** - Veb-saytning dizayni uchun CSS framework.

## O'rnatish

Loyihani mahalliy muhitda ishga tushirish uchun quyidagi qadamlarni bajaring:

1. Repozitoriyani klonlang:
   ```bash
   git clone https://github.com/foydalanuvchi/Watches-Shop.git
   cd Watches-Shop

2. Virtual muhit yarating va faollashtiring:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows uchun: venv\Scripts\activate

3. Zarur paketlarni o'rnating:
    ```bash
    pip install -r requirements.txt

4. Ma'lumotlar bazasini migratsiya qiling:
    ```bash
    python manage.py migrate

5. Superuser yarating (admin paneliga kirish uchun):
    ```bash
    python manage.py createsuperuser

6. Loyihani ishga tushiring:
    ```bash
    python manage.py runserver

7. Veb-saytni brauzerda oching:
    ```bash
    http://127.0.0.1:8000/

8. Admin panel ga kirish:
    ```bash
    http://127.0.0.1:8000/admin/