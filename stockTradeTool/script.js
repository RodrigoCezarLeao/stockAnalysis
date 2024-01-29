const addNewTickerTable = () => {
    const table = document.createElement("table");

    // CAPTION
    const caption = document.createElement("caption");
    const inputTicker = document.createElement("input");
    caption.appendChild(inputTicker);
    table.appendChild(caption);

    // THEAD
    const thead = document.createElement("thead");
    const tr = document.createElement("tr");
    const th1 = document.createElement("th");
    th1.textContent = "Type";
    const th2 = document.createElement("th");
    th2.textContent = "Price";
    const th3 = document.createElement("th");
    th3.textContent = "Amount";
    const th4 = document.createElement("th");
    th4.textContent = "Total";

    tr.appendChild(th1);
    tr.appendChild(th2);
    tr.appendChild(th3);
    tr.appendChild(th4);
    thead.appendChild(tr);
    table.appendChild(tr);


    // TBODY
    table.appendChild(document.createElement("tbody"));

    // FOOTER
    const footer = document.createElement("tbody");
    const f_tr1 = document.createElement("tr");
    const f_tr1_td1 = document.createElement("td");
    f_tr1_td1.colSpan = 3;
    const f_tr1_td2 = document.createElement("td");
    const span = document.createElement("span");
    span.className = "material-symbols-outlined";
    span.textContent = "add_circle";
    span.addEventListener("click", () => {addNewRecord('buy')})
    f_tr1_td2.appendChild(span);

    f_tr1.appendChild(f_tr1_td1);
    f_tr1.appendChild(f_tr1_td2);
    footer.appendChild(f_tr1);

    const f_tr2 = document.createElement("tr");
    const f_tr2_td1 = document.createElement("td");
    f_tr2_td1.colSpan = 2;
    f_tr2_td1.textContent = "Balance";
    const f_tr2_td2 = document.createElement("td");
    f_tr2_td2.colSpan = 2;

    f_tr2.appendChild(f_tr2_td1);
    f_tr2.appendChild(f_tr2_td2);
    footer.appendChild(f_tr2);
    table.appendChild(footer);
    
    document.getElementsByTagName("main")?.[0].appendChild(table);
}

const addNewRecord = (type, tbody = null, price = null, amount = null) => {
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
    select.selectedOptions = type;
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
    if (price)
        inputNumber.value = price;

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
    if (amount)
        inputNumber2.value = amount;

    td3.appendChild(inputNumber2);
    tr.appendChild(td3);

    const td4 = document.createElement("td");    
    if (price && amount)
        td4.textContent = `$ ${type === "sell" ? "-" : ""}${(price * amount).toFixed(2)}`;
    tr.appendChild(td4);

    const td5 = document.createElement("td");
    const span = document.createElement("span");
    span.className = "material-symbols-outlined";
    span.textContent = "delete";
    span.addEventListener("click", () => {tr.remove();});

    td5.appendChild(span);
    tr.appendChild(td5);

    tbody ? tbody.appendChild(tr) : window.event.srcElement.offsetParent.offsetParent.children[2].appendChild(tr);
    
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
    for (let row of table.children[2].children){
        let totalPrice = row.children[3].textContent.replace("$", "");
        total += Number(totalPrice);
    }
    
    table.children[3].children[1].children[1].textContent = `${total <= 0 ? "+" : "-"} $ ${(-1 * total).toFixed(2).replace("-","")}`;
    table.children[3].children[1].children[1].className = !total ? "" : total > 0 ? "buy" : "sell";
}

const addLoadedTickerTable = (tickerInfo) => {
    addNewTickerTable();
    
    let lastTable = document.getElementsByTagName("main")?.[0].children;
    lastTable = lastTable[lastTable.length - 1];
    
    lastTable.children[0].children[0].value = tickerInfo.ticker;

    for (let tr of tickerInfo.result){        
        addNewRecord(tr.type, lastTable.children[2], tr.unitValue, tr.amount);
        updateBalance(lastTable);
    }

}