package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type Message struct {
	Text       string `json:"text"`
	EndSession bool   `json:"end_session"`
}

type YandexStation struct {
	Response Message `json:"response"`
	Version  string  `json:"version"`
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/station/", handleYandexStation)
	log.Println("server started")
	log.Fatal(http.ListenAndServe("0.0.0.0:8000", mux))
}

func debtMessage(years, beginDate string) (string, error) {
	input, err := getInput(beginDate, years)
	if err != nil {
		return "", fmt.Errorf("failed to parse debtInfo: %w", err)
	}
	info := calculate(input)
	return makeResponse(info), nil
}


func handleYandexStation(w http.ResponseWriter, r *http.Request) {
	queryParams := r.URL.Query()
	years := queryParams.Get("years")
	beginDate := queryParams.Get("beginDate")
	text, err := debtMessage(years, beginDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	msg := Message{Text: text, EndSession: true}
	resp := YandexStation{Response: msg, Version: "1.0"}
	js, err := json.Marshal(resp)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	if _, err := w.Write(js); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
