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
            type: "sell",
            date: "2024-02-03",
            amount: 100,
            price: 1000,
        },
        {
            type: "buy",
            date: "2024-02-04",
            amount: 50,
            price: 20,
        },
    ]

}

const calculateRemainingStockAmount = (tradingHistory) => {
    totalStocks = 0;

    for(let record of tradingHistory){
        let recordStocks = record.type === "buy" ? record.amount : record.type === "sell" ? record.amount * -1 : 0;
        totalStocks += recordStocks;
    }

    return totalStocks;
}


const calculateAveragePrice = (tradingHistory) => {
    avgPrice = 0;
    totalStock = 0;
    
    for(let record of tradingHistory){
        if (record.type === "buy"){
            if (avgPrice === 0 ){
                avgPrice = record.price;
                totalStock = record.amount;
            }
            else {
                avgPrice = ((avgPrice * totalStock) + (record.price * record.amount)) / (totalStock + record.amount);
                totalStock += record.amount;
            }
        }else if (record.type === "sell"){
            totalStock -= record.amount;
        }
    }
    
    return avgPrice;    
}


result = calculateRemainingStockAmount(singleExampleTwo.tradingHistory);
result1 = calculateAveragePrice(singleExampleTwo.tradingHistory);

console.log("🚀 ~ result:", result);
console.log("🚀 ~ result1:", result1);


// Fazer split, inplit de ações e histórico de dividendos