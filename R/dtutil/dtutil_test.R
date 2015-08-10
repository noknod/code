source('dtutil.R')



# date transform
test_dates <- function() {
  rm(vdate)
  vdate <- as.Date('2015.05.31', '%Y.%m.%d')

  month.add(vdate, -1)
  month.add(vdate, 0)
  month.add(vdate, 1)
  
  month.firstday(vdate, -1)
  month.firstday(vdate, 0)
  month.firstday(vdate, 1)
  
  month.lastday(vdate)
  month.lastday(vdate)
  month.lastday(vdate)

  month.period(vdate, -1, 1)
  month.period(vdate, -1, 1, allowReverse=TRUE)
  month.period(vdate, 1, allowReverse=TRUE)
  month.period(vdate, start=-1, end=0)
  month.period(vdate, start=1, end=0, allowReverse=TRUE)
  month.period(vdate, -1)
  month.period(vdate, start=-2, end=-1)
  month.period(vdate, 0)
  
  vdate <- as.Date('2020-02-29')  
  year.add(vdate, 1)
  year.firstday(vdate)
  year.lastday(vdate)
  year.period(vdate, start=-2, end=-1)
}



# read
test_read <- function() {
  rm(vdata, dates)
  vdata = data.frame(Day=c('Friday, December 31 2011',
                           'Sunday, January 01 2012', 
                           'Monday, January 02 2012', 
                           'Tuesday, January 03 2012',
                           'Wednesday, January 04 2012',
                           'Thursday, January 05 2012',
                           'Friday, January 06 2012',
                           'Saturday, January 07 2012'),
                     stringsAsFactors=FALSE)
  field = 'Day'
  template = '%A, %B %d %Y'
  dates <- read.dates(vdata, template, field)
  dates
  
  read.years(dates)
  read.months(dates)
  read.days(dates)
  read.weekdays(dates)
}



# subset
test_subset <- function() {
  rm(vdata, dates, since, along)
  vdata = data.frame(Date=seq(from=as.Date('2014-12-01'), 
                              to=as.Date('2015-02-28'), by=1))#, length.out=10))

  field <- 'Date'
  since <-  NA
  along <- NA
  subset.date(vdata, since=since, along=along)
  since <-  as.Date('2015-02-27')
  along <- NA
  subset.date(vdata[[field]], since=since, along=along)
  subset.date(vdata, since=since, along=along, field=field)
  since <-  NA
  along <- as.Date('2014-12-02')
  subset.date(vdata[[field]], since=since, along=along)
  subset.date(vdata, since=since, along=along, field=field)
  since <-  as.Date('2015-01-04')
  along <- as.Date('2015-01-08')
  subset.date(vdata[[field]], since=since, along=along)
  subset.date(vdata, since=since, along=along, field=field)
  
  vdate <- as.Date('2015-01-04')
  since <-  NA
  along <-  NA
  subset.month(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.month(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  0
  along <-  NA
  subset.month(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.month(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  0
  along <-  0
  subset.month(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.month(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  1
  along <-  -1
  subset.month(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.month(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  0
  along <-  0
  subset.month(vdata[[field]], vdate=vdate, since=since, along=along, 
               sinceDay='current', alongDay='current')
  since <-  1
  along <-  0
  subset.month(vdata, vdate=vdate, since=since, along=along, 
               field=field, sinceDay='current', alongDay='current')

  since <-  NA
  along <-  NA
  subset.year(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.year(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  0
  along <-  NA
  subset.year(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.year(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  0
  along <-  0
  subset.year(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.year(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  1
  along <-  -1
  subset.year(vdata[[field]], vdate=vdate, since=since, along=along)
  subset.year(vdata, vdate=vdate, since=since, along=along, field=field)
  since <-  0
  along <-  0
  subset.year(vdata[[field]], vdate=vdate, since=since, along=along, 
               sinceDay='current', alongDay='current')
  since <-  0
  along <-  1
  subset.year(vdata, vdate=vdate, since=since, along=along, 
               field=field, sinceDay='current', alongDay='current')

  rm(vdata, dates, since, along)
}



# factor
test_factor <- function() {
  rm(vdata, dates, since, along, field)
  vdata = data.frame(Date=seq(as.Date('2014-12-01'), by=1, length.out=80))
  field = 'Date'
  
  extract.year(vdata[[field]])
  extract.year(vdata, field)
  extract.year(vdata[[field]], seqtype='continius')
  extract.year(vdata, field, 'continius', TRUE)

  extract.month(vdata[[field]])
  extract.month(vdata, field)
  extract.month(vdata, field, 'continius')
  extract.month(vdata, field, 'continius', TRUE)
  extract.month(vdata, field, 'year')
  extract.month(vdata, field, 'year', TRUE)
  
  extract.wday(vdata[[field]])
  extract.wday(vdata, field)
  extract.wday(vdata, field, 'continius')
  extract.wday(vdata, field, 'continius', TRUE)
  extract.wday(vdata, field, 'month')
  extract.wday(vdata, field, 'month', TRUE)
  extract.wday(vdata, field, 'year')
  extract.wday(vdata, field, 'year', TRUE)

  extract.fact(vdata[[field]])
  extract.fact(vdata, field)
  by <- 'month'
  extract.fact(vdata, field, by=by)
  by <- 'year'
  extract.fact(vdata, field, by=by)
  fields <- c('month', 'wday')
  by <- 'month'
  extract.fact(vdata, field, fields=fields, by=by)
  by <- 'year'
  extract.fact(vdata, field, fields=fields, by=by)
  fields <- c('wday')
  by <- 'month'
  extract.fact(vdata, field, fields=fields, by=by)
  by <- 'year'
  extract.fact(vdata, field, fields=fields, by=by)
  fields <- c('month')
  by <- 'month'
  extract.fact(vdata, field, fields=fields, by=by)
  by <- 'year'
  extract.fact(vdata, field, fields=fields, by=by)
  fields <- c('year', 'month')
  by <- 'month'
  extract.fact(vdata, field, fields=fields, by=by)
  by <- 'year'
  extract.fact(vdata, field, fields=fields, by=by)
  fields <- c('year', 'wday')
  by <- 'month'
  extract.fact(vdata, field, fields=fields, by=by)
  by <- 'year'
  extract.fact(vdata, field, fields=fields, by=by)
  
  fields <- c('year', 'month', 'wday')
  asFactors <- TRUE
  vlevels <- c('Mon', 'Tus', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun')
}



# na
test_na <- function () {
  vdata <- data.frame(v1=c(NA, NA, 3, 6, 5, 4),
                       v2=c(1, 7, 3, 6, NA, NA),
                       v3=c(1, 7, NA, NA, 3, 6))
  na.interpolate(vdata)
}




# aggregate
test_aggregate <- function() {
    rm(vdata, fields)
    vdata = data.frame(Date=seq(as.Date('2014-12-01'), by=1, length.out=80),
                       Val=seq(1, 80)
                       )
    vdata$f1 <- as.vector(rbind(rep(1, 40), rep(2, 40)))
    f2 <- c()
    for (i in 1:20) {f2 <- rbind(f2, 1)}
    for (i in 1:30) {f2 <- rbind(f2, 2)}
    for (i in 1:30) {f2 <- rbind(f2, 3)}
    vdata$f2 <- as.vector(f2)
    vdata
    by = c('f1', 'f2')
    cnt.fact(vdata, by)
    
    fields = c('Val')    
    by = c('f1')
    aggr.fact(vdata, fields, by, sum)
    by = c('f1', 'f2')
    aggr.fact(vdata, fields, by, sum)
    aggr.fact(vdata, fields, by, median)
    fieldDate <- 'Date'
    aggr.fact(vdata, fields, by, median, fieldDate)
}