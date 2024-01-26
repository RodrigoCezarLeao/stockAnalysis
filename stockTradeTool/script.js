const addNewRecord = (type) => {
    const tr = document.createElement("tr");
    tr.className = type;

    const td1 = document.createElement("td");
    const select = document.createElement("select");
    const option_buy = document.createElement("option");
    option_buy.value = "buy";
    option_buy.textContent = "Buy";
    const option_sell = document.createElement("option");
    option_sell.value = "sell";
    option_sell.textContent = "Sell";
    select.className = type;
    select.addEventListener("change", () => {
        changeRecordType(tr, select.value);
        calculateTotalInRow(tr, select.value);        
        updateBalance(tr.offsetParent);
    });

    select.appendChild(option_buy);
    select.appendChild(option_sell);
    td1.appendChild(select);
    tr.appendChild(td1);


    const td2 = document.createElement("td");
    const inputNumber = document.createElement("input");
    inputNumber.type = "number";
    inputNumber.step = 0.01;
    inputNumber.className = type;
    inputNumber.addEventListener("change", () => {
        calculateTotalInRow(tr, select.value);        
        updateBalance(tr.offsetParent);
    });

    td2.appendChild(inputNumber);
    tr.appendChild(td2);

    const td3 = document.createElement("td");
    const inputNumber2 = document.createElement("input");
    inputNumber2.type = "number";
    inputNumber2.step = 1;
    inputNumber2.className = type;
    inputNumber2.addEventListener("change", () => {
        calculateTotalInRow(tr, select.value);
        updateBalance(tr.offsetParent);
    });

    td3.appendChild(inputNumber2);
    tr.appendChild(td3);

    const td4 = document.createElement("td");
    tr.appendChild(td4);

    const td5 = document.createElement("td");
    const span = document.createElement("span");
    span.className = "material-symbols-outlined";
    span.textContent = "delete";

    td5.appendChild(span);
    tr.appendChild(td5);

        
    document.getElementsByTagName("tbody")[0].appendChild(tr);
    
}

const changeRecordType = (tr, value) => {    
    tr.className = value;
    tr.children[0].children[0].className = value;
    tr.children[1].children[0].className = value;
    tr.children[2].children[0].className = value;
}


const calculateTotalInRow = (tr, type) => {
    let price = tr.children[1].children[0].value;
    let amount = tr.children[2].children[0].value;
    let total = 0;

    if (price && amount)
        total = Number(price) * Number(amount);
    
    tr.children[3].textContent = `$ ${type === "sell" ? "-" : ""}${total.toFixed(2)}`;
}

const updateBalance = (table) => {
    let total = 0;
    for (let row of table.children[1].children){
        let totalPrice = row.children[3].textContent.replace("$", "");
        total += Number(totalPrice);
    }
    
    table.children[2].children[1].children[1].textContent = `${total <= 0 ? "+" : "-"} $ ${(-1 * total).toFixed(2).replace("-","")}`;
    table.children[2].children[1].children[1].className = !total ? "" : total > 0 ? "sell" : "buy";
}