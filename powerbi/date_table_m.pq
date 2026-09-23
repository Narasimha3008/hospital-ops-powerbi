// Power Query (M) — Date dimension table
// In Power BI Desktop: Get Data > Blank Query > Advanced Editor > paste.
// Then Close & Apply, and mark as date table (Table tools > Mark as date table).

let
    StartDate = #date(2024, 1, 1),
    EndDate   = #date(2026, 12, 31),
    DayCount  = Duration.Days(EndDate - StartDate) + 1,
    DateList  = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    ToTable   = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    AddYear      = Table.AddColumn(ToTable, "Year", each Date.Year([Date]), Int64.Type),
    AddQuarter   = Table.AddColumn(AddYear, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddMonthNum  = Table.AddColumn(AddQuarter, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddMonth     = Table.AddColumn(AddMonthNum, "Month", each Date.ToText([Date], "MMMM"), type text),
    AddMonthYear = Table.AddColumn(AddMonth, "MonthYear", each Date.ToText([Date], "MMM yyyy"), type text),
    AddDayName   = Table.AddColumn(AddMonthYear, "DayName", each Date.ToText([Date], "dddd"), type text),
    AddIsWeekend = Table.AddColumn(AddDayName, "IsWeekend", each Date.DayOfWeek([Date], Day.Sunday) >= 5, type logical),
    SetTypes  = Table.TransformColumnTypes(AddIsWeekend, {{"Date", type date}})
in
    SetTypes
