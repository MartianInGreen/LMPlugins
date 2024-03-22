setInterval(() => {
    menu = document.getElementsByClassName("py-2 max-h-[300px] overflow-auto")[0];

    if (menu) {
        menu.style.maxHeight = "600px";
        menu.style.overflow = "auto";
    }
}, 100);