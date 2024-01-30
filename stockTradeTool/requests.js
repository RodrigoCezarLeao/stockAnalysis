const findTickerPrice = async (ticker) => {
    if(!ticker)
        return false;

    let resp = await fetch("http://127.0.0.1:5000/stock_price?stock=@stock".replace("@stock", ticker));
    let data = await resp.json();    
    return Number(data.price.replace(",", "."));
}