use chrono::Local;
use clap::Parser;
use reqwest::blocking::get;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::{thread, time::Duration};

#[derive(Debug, Serialize, Deserialize)]
struct RawPrice {
    currency: String,
    #[serde(rename = "amount")]
    value: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct Price {
    timestamp: String,
    currency: String,
    value: f64,
}

fn parse_price(raw_price: Value) -> Price {
    let data: &Value = &raw_price["data"];
    let raw_price: RawPrice = serde_json::from_value(data.clone()).unwrap();
    Price {
        currency: raw_price.currency,
        value: raw_price.value.parse().unwrap(),
        timestamp: Local::now().format("%Y-%m-%dT%H:%M:%S").to_string(),
    }
}

fn get_current_price() -> Result<Price, reqwest::Error> {
    let raw: serde_json::Value = get("https://api.coinbase.com/v2/prices/BTC-USD/spot")?.json()?;
    let price = parse_price(raw);
    Ok(price)
}

#[derive(Debug, Parser)]
struct Cli {
    #[arg(short, long, default_value_t = 5)]
    freq: u64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Cli::parse();
    loop {
        let price = get_current_price()?;
        let line = serde_json::to_string(&price)?;
        println!("{}", line);

        thread::sleep(Duration::from_secs(args.freq))
    }
}
