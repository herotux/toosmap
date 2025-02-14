document.querySelectorAll('.icon-toggle').forEach(item => {
    item.addEventListener('click', event => {
        const parentRow = item.closest('tr'); // یافتن ردیف والد
        let nextRow = parentRow.nextElementSibling; // ردیف بعدی
        let isHidden = false;

        // بررسی وضعیت نمایش اولین زیردسته
        if (nextRow && nextRow.classList.contains('submenu')) {
            isHidden = nextRow.style.display === 'none';
        }

        // تغییر وضعیت تمام زیردسته‌های مرتبط
        while (nextRow && nextRow.classList.contains('submenu')) {
            nextRow.style.display = isHidden ? 'table-row' : 'none';
            nextRow = nextRow.nextElementSibling;
        }

        // تغییر آیکون +/-
        item.textContent = isHidden ? '-' : '+';
    });
});

document.querySelectorAll('.delete-category').forEach(item => {
    item.addEventListener('click', event => {
        if (!confirm('آیا مطمئن هستید که می‌خواهید این دسته‌بندی را حذف کنید؟')) {
            event.preventDefault();
        }
    });
});