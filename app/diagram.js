function createChart() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var chart = sheet.newChart()
        .setChartType(Charts.ChartType.COLUMN)
        .addRange(sheet.getRange("A2:C2"))
        .setPosition(5, 3, 0, 0)
        .build();
    sheet.insertChart(chart);
  }
