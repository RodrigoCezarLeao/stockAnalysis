const singleExample = {
    ticker: "TAEE4",
    currentPrice: 12.27,
    // averagePrice: 12.56,
    // stockAmount: 17,
    tradingHistory: [
        {
            type: "buy",
            date: "2024-02-01",
            amount: 1,
            price: 5,
        },
        {
            type: "buy",
            date: "2024-02-02",
            amount: 3,
            price: 6,
        },
        {
            type: "buy",
            date: "2024-02-03",
            amount: 1,
            price: 7,
        },
        {
            type: "sell",
            date: "2024-02-04",
            amount: 2,
            price: 6.5,
        },
    ]

}
const singleExampleTwo = {
    ticker: "EXEM4",
    currentPrice: 12.27,
    // averagePrice: 12.56,
    // stockAmount: 17,
    tradingHistory: [
        {
            type: "buy",
            date: "2024-02-01",
            amount: 200,
            price: 14,
        },
        {
            type: "buy",
            date: "2024-02-02",
            amount: 300,
            price: 15,
        },
        {
            type: "split",
            date: "2024-02-03",
            amount: 10,
            price: 0,
        },
        {
            type: "sell",
            date: "2024-02-04",
            amount: 100,
            price: 1,
        },
        {
            type: "buy",
            date: "2024-02-05",
            amount: 50,
            price: 0.5,
        },
        {
            type: "inplit",
            date: "2024-02-06",
            amount: 2,
            price: 0,
        },
    ]

}

const calculateRemainingStockAmount = (tradingHistory) => {
    totalStocks = 0;

    for(let record of tradingHistory){
        let recordStocks = 0;
        switch (record.type){
            case 'buy':
                recordStocks = record.amount;
                totalStocks += recordStocks;
                break;
            case 'sell':
                recordStocks = record.amount * -1;
                totalStocks += recordStocks;
                break;
            case 'split':
                totalStocks = totalStocks * record.amount;                
                break;
            case 'inplit':                
                totalStocks = totalStocks / record.amount;
                break;
            default:
                break;
        }        
    }

    return totalStocks;
}


const calculateAveragePrice = (tradingHistory) => {
    avgPrice = 0;
    totalStock = 0;
    
    for(let record of tradingHistory){
        switch (record.type){
            case 'buy':
                if (avgPrice === 0 ){
                    avgPrice = record.price;
                    totalStock = record.amount;
                }
                else {
                    avgPrice = ((avgPrice * totalStock) + (record.price * record.amount)) / (totalStock + record.amount);
                    totalStock += record.amount;
                }
                break;
            case 'sell':
                totalStock -= record.amount;
                break;
            case 'split':
                totalStock = totalStock * record.amount;
                avgPrice = avgPrice / record.amount;
                break;
            case 'inplit':
                totalStock = totalStock / record.amount;
                avgPrice = avgPrice * record.amount;
                break;
            default:
                break;
        }        
    }
    
    return avgPrice;
}

const calculateTotalInvestmentCost = (tradingHistory) => {
    let total = 0;
    for(let record of tradingHistory){
        if (record.type === "buy")
            total += record.amount * record.price;
    }

    return total;
}


result = calculateRemainingStockAmount(singleExampleTwo.tradingHistory);
result1 = calculateAveragePrice(singleExampleTwo.tradingHistory);
result3 = calculateTotalInvestmentCost(singleExampleTwo.tradingHistory);

console.log("🚀 ~ result:", result);
console.log("🚀 ~ result1:", result1);
console.log("🚀 ~ result3:", result3);


// Fazer split, inplit de ações e histórico de dividendos