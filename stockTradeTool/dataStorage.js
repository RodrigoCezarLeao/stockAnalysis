const saveAll = () => {
    localStorage.setItem("ludmilo_data", JSON.stringify(wallets));
}

const loadAll = () => {
    const walletsLoaded = localStorage.getItem("ludmilo_data");
    wallets = walletsLoaded ? JSON.parse(walletsLoaded) : [];

    if (wallets)
        renderAside_UI();
}

loadAll();