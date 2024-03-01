let wallets = [];

const createNewWallet = () => {
    const newWallet = {
        createdAt: new Date().getTime().toString(),
        title: "New Wallet",
        content: [],
        custodian: []
    };

    wallets.push(newWallet);
    renderAside_UI();    
}

const createNewWalletCategory = (wallet) => {
    const newCategory = {
        createdAt: new Date().getTime().toString(),
        title: "New Category",
        content: [],
    }

    wallet.content.push(newCategory);
}


const openWalletContent_UI = (event) => {
    const walletCreatedAt = event?.target?.id ?? event["wallet.id"];
    const wallet = wallets.find(x => x.createdAt === walletCreatedAt);

    const contentContainer = document.getElementById("current_wallet_content_container");
    if (wallet && !contentContainer.innerHTML.includes(wallet.createdAt)){
        contentContainer.innerHTML = "";

        const div = document.createElement("div");

        const titleInput = document.createElement("input");
        titleInput.value = wallet.title;
        div.appendChild(titleInput);

        const updateButton = document.createElement("button");
        updateButton.textContent = "Update";
        updateButton.addEventListener("click", (wallet) => {            
            wallets.find(x => x.createdAt === walletCreatedAt).title = titleInput.value;
            renderAside_UI();
        });
        div.appendChild(updateButton);

        contentContainer.appendChild(div);


        const div2 = document.createElement("div");
        const newCategoryButton = document.createElement("button");
        newCategoryButton.textContent = "New category";
        newCategoryButton.addEventListener("click", () => {
            createNewWalletCategory(wallets.find(x => x.createdAt === walletCreatedAt));
            openWalletContent_UI({ "wallet.id": wallet.createdAt });
        });
        div2.appendChild(newCategoryButton);
        contentContainer.appendChild(div2);


        for (let category of wallet.content){
            const div3 = document.createElement("div");
            const categoryInput = document.createElement("input");
            categoryInput.value = category.title;
            div3.appendChild(categoryInput);
            contentContainer.appendChild(div3);
        }
    }

}

const renderAside_UI = () => {
    const ul = document.getElementById("wallets_list");
    ul.innerHTML = "";

    for (let wallet of wallets) {
        const li = document.createElement("li");
        li.textContent = wallet.title;
        li.id = wallet.createdAt;
        ul.appendChild(li);
    }
}