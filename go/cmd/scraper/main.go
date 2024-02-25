package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"time"
)

type GetPriceResponse struct {
	Data struct {
		Currency string      `json:"currency"`
		Amount   json.Number `json:"amount"`
	} `json:"data"`
}

type Price struct {
	Currency  string  `json:"currency"`
	Value     float64 `json:"value"`
	Timestamp string  `json:"timestamp"`
}

func getCurrentPrice() Price {
	rawResp, err := http.Get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
	// TODO: retry and handle
	if err != nil {
		panic(err)
	}

	timestamp := time.Now().Format("2006-01-02T15:04:05")
	data, _ := io.ReadAll(rawResp.Body)

	var resp GetPriceResponse
	err = json.Unmarshal([]byte(data), &resp)

	if err != nil {
		panic(err)
	}
	value, _ := resp.Data.Amount.Float64()
	value = float64(int(value*100)) / 100 // allow at most 2 decimals

	return Price{Value: value, Timestamp: timestamp, Currency: resp.Data.Currency}

}

func main() {
	freq := flag.Int("freq", 5, "Frequency in seconds to request the price")

	flag.Parse()

	for {
		price := getCurrentPrice()
		time.Sleep(time.Duration(*freq) * time.Second)
		out, err := json.Marshal(price)
		if err != nil {
			panic(err)
		}

		fmt.Println(string(out))
	}
}
