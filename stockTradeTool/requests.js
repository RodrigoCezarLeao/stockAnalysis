const findTickerPrice = async (ticker) => {
    if(!ticker)
        return false;

    let resp = await fetch("https://manage-group-api.vercel.app/stock_price?stock=@stock".replace("@stock", ticker));
    // let resp = await fetch("http://127.0.0.1:5000/stock_price?stock=@stock".replace("@stock", ticker));
    
    let data = await resp.json();    
    return data.currentPrice === -1 ? -1 : Number(data.currentPrice.replace(",", "."));
}