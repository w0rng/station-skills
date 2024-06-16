package main

import (
	"fmt"
	"strconv"
	"time"
)

type DebtInfo struct {
	Years  int
	Months int
	Days   int
	Hours  int
}

type InputData struct {
	beginDate time.Time
	Years     int
}

func calculate(input InputData) DebtInfo {
	endDebt := input.beginDate.AddDate(input.Years, 0, 0)
	hours := int(time.Until(endDebt).Hours())
	const (
		hoursPerDay   = 24
		hoursPerMonth = 24 * 30
		hoursPerYear  = 24 * 365
	)

	years := hours / hoursPerYear
	hours %= hoursPerYear

	months := hours / hoursPerMonth
	hours %= hoursPerMonth

	days := hours / hoursPerDay
	hours %= hoursPerDay

	return DebtInfo{Years: years, Months: months, Days: days, Hours: hours}
}

func pluralize(number int, one, few, many string) string {
	if number%10 == 1 && number%100 != 11 {
		return one
	} else if (number%10 >= 2 && number%10 <= 4) && !(number%100 >= 12 && number%100 <= 14) {
		return few
	} else {
		return many
	}
}

func makeResponse(info DebtInfo) string {
	yearsWord := pluralize(info.Years, "год", "года", "лет")
	monthsWord := pluralize(info.Months, "месяц", "месяца", "месяцев")
	daysWord := pluralize(info.Days, "день", "дня", "дней")
	hoursWord := pluralize(info.Hours, "час", "часа", "часов")

	template := "Осталось платить %d %s, %d %s, %d %s, %d %s."
	return fmt.Sprintf(template, info.Years, yearsWord, info.Months, monthsWord, info.Days, daysWord, info.Hours, hoursWord)
}

func getInput(date string, years string) (InputData, error) {
	dateDebt, err := time.Parse("2006-01-02", date)
	if err != nil {
		return InputData{}, fmt.Errorf("failed to parse dateDebt: %w", err)
	}
	yearCount, err := strconv.Atoi(years)
	if err != nil {
		return InputData{}, fmt.Errorf("failed to parse yearCount: %w", err)
	}
	return InputData{beginDate: dateDebt, Years: yearCount}, nil
}
