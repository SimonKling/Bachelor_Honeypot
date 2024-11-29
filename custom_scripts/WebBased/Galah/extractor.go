package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

type LogEntry struct {
	Error        *Error        `json:"error,omitempty"`
	EventTime    string        `json:"eventTime"`
	SrcIP        string        `json:"srcIP"`
	HttpRequest  *HttpRequest  `json:"httpRequest,omitempty"`
	HttpResponse *HttpResponse `json:"httpResponse,omitempty"`
}

type Error struct {
	Msg string `json:"msg"`
}

type HttpRequest struct {
	Body    string `json:"body"`
	Method  string `json:"method"`
	Request string `json:"request"`
}

type HttpResponse struct {
	Body string `json:"body"`
}

func main() {
	outputDir := flag.String("output", "output/", "Directory for output CSV files")
	flag.Parse()

	inputFiles := []string{
		"./Galah/AzureGalah_export.json",
		"./Galah/GoogleGalah_export.json",
		"./Galah/OracleGalah_export.json",
		"./Galah/DigitalOceanGalah_export.json",
	}

	os.MkdirAll(*outputDir, os.ModePerm)

	for _, inputFile := range inputFiles {
		file, _ := os.Open(inputFile)
		defer file.Close()

		outputFileName := filepath.Join(*outputDir, filepath.Base(inputFile)+".csv")
		outputFile, _ := os.Create(outputFileName)
		defer outputFile.Close()

		writer := csv.NewWriter(outputFile)
		defer writer.Flush()

		header := []string{"EventTime", "SrcIP", "HasError", "Request Body", "Method", "Request Path", "Response Body"}
		_ = writer.Write(header)

		scanner := bufio.NewScanner(file)
		lineNumber := 0
		count := 0

		for scanner.Scan() {
			lineNumber++
			line := scanner.Text()
			var entry LogEntry

			_ = json.Unmarshal([]byte(line), &entry)

			hasError := "false"
			if entry.Error != nil {
				hasError = "true"
			}

			requestBody := ""
			method := ""
			requestPath := ""
			if entry.HttpRequest != nil {
				requestBody = entry.HttpRequest.Body
				method = entry.HttpRequest.Method
				requestPath = entry.HttpRequest.Request
			}

			responseBody := ""
			if entry.HttpResponse != nil {
				responseBody = entry.HttpResponse.Body
			}

			row := []string{
				entry.EventTime,
				entry.SrcIP,
				hasError,
				requestBody,
				method,
				requestPath,
				responseBody,
			}

			_ = writer.Write(row)
			count++

		
		}

		fmt.Printf("Finished processing file '%s'. Total records: %d\n", inputFile, count)
	}
}
