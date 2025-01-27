document.querySelectorAll('.icon-toggle').forEach(item => {
    item.addEventListener('click', event => {
        const submenu = item.nextElementSibling; // Adjusted to select the submenu correctly
        submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block'; // Toggle visibility
        item.textContent = item.textContent === '+' ? '-' : '+'; // Change icon
    });
});

document.querySelectorAll('.delete-category').forEach(item => {
    item.addEventListener('click', event => {
        if (!confirm('آیا مطمئن هستید که می‌خواهید این دسته‌بندی را حذف کنید؟')) {
            event.preventDefault();
        }
    });
});
