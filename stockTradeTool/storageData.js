const saveInterfaceData = () => {
    const main = document.getElementsByTagName("main")?.[0];

    let pageResult = [];
    
    for (let table of main.children){
        let ticker = table.children[0].children[0].value.toUpperCase();

        if (!ticker)
            continue;

        let tickerResult = {
            ticker: ticker,
            result: [],
        };

        for (let tr of table.children[2].children){
            let type = tr.children[0].children[0].value;
            let unitValue = tr.children[1].children[0].value;
            let amount = tr.children[2].children[0].value;

            let trResult = {
                "type": type,
                "unitValue": Number(unitValue),
                "amount": Number(amount),
            }

            tickerResult.result.push(trResult);
        }

        pageResult.push(tickerResult);
    }

    window.localStorage.setItem("stock_analysis-save", JSON.stringify(pageResult));
}

const loadAllInterfaceData = () => {
    const pageResult = JSON.parse(window.localStorage.getItem("stock_analysis-save"));

    if (pageResult && pageResult.length > 0){
        for (let table of pageResult){
            addLoadedTickerTable(table);        
        }
    }
}

loadAllInterfaceData();