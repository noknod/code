require('lubridate')
require('VIM')
require('dplyr')



# date transform
month.add <- function(vdate, num) {
  # 
  new_date <- vdate + months(num)
  if (is.na(new_date)) {
    for(delta in 28:(day(vdate) - 1) - 27) {
      new_date <- vdate - delta + months(num)
      if (!is.na(new_date)) {return(new_date)}
    }
  }
  return(new_date)
}



month.firstday <- function(vdate) {
  # 
  return(as.Date(as.character(vdate, '%Y%m%01'), '%Y%m%d'))
}



month.lastday <- function(vdate) {
  # 
  for(delta in 31:28) {
    str_date <- paste('%Y%m%', delta, sep='')
    new_date <- as.Date(as.character(vdate, str_date), '%Y%m%d')
    if (!is.na(new_date)) {return(new_date)}
  }
}



month.period <- function(vdate, end, start=0, allowReverse=FALSE) {
  # 
  if (start != 0) {start_date <- month.add(vdate, start)}
  else {start_date <- vdate}
  if (end != 0) {end_date <- month.add(vdate, end)}
  else {end_date <- vdate}
  if (start_date > end_date & !allowReverse) {
    tmp <- end_date
    end_date <- start_date
    start_date <- tmp
  }
  return(c(start_date, end_date))
}



year.add <- function(vdate, num) {
  # 
  new_date <- vdate + years(num)
  if (is.na(new_date)) {
    new_date <- vdate - 1 + years(num)
  }
  return(new_date)
}



year.firstday <- function(vdate) {
  # 
  return(as.Date(as.character(vdate, '%Y%01%01'), '%Y%m%d'))
}



year.lastday <- function(vdate) {
  # 
  return(as.Date(as.character(vdate, '%Y%12%31'), '%Y%m%d'))
}



year.period <- function(vdate, end, start=0, allowReverse=FALSE) {
  # 
  if (start != 0) {start_date <- year.add(vdate, start)}
  else {start_date <- vdate}
  if (end != 0) {end_date <- year.add(vdate, end)}
  else {end_date <- vdate}
  if (start_date > end_date & !allowReverse) {
    tmp <- end_date
    end_date <- start_date
    start_date <- tmp
  }
  return(c(start_date, end_date))
}



read.dates <- function(vdata, template, field=NA) {
  # transform the filed Day into a Date object
  
  ### This will give NA(s) in some locales; setting the C locale
  ### as in the commented lines will overcome this on most systems.
  lct <- Sys.getlocale("LC_TIME"); Sys.setlocale("LC_TIME", "C")
  
  ### transform
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  dates <- as.Date(dates, template)
  
  ### restore locale
  Sys.setlocale("LC_TIME", lct)
  
  return(dates)
}



read.years <-  function(vdata, field=NA) {
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  return(year(vdata))
}



read.months <-  function(vdata, field=NA) {
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  return(month(vdata))
}



read.days <-  function(vdata, field=NA) {
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  return(day(vdata))
}



read.weekdays <-  function(vdata, field=NA) {
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  return(wday(vdata))
}



# subset
subset.date <- function (vdata, since=NA, along=NA, field=NA) {
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  indexes <- rep(x=TRUE, length.out=length(dates))
  if (!is.na(since)) {indexes = indexes & (dates > since - 1)}
  if (!is.na(along)) {indexes = indexes & (dates < along + 1)}
  return(subset(x=vdata, subset=indexes))
}



subset.month <- function (vdata, vdate=NA, since=NA, along=NA, field=NA,
                          sinceDay='first', alongDay='last') {
  # Day in 'first', 'current', 'last'
  if (is.na(vdate)) {
    return(vdata)
  }
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  if (is.na(since)) {since_date <- dates[1]}
  else {since_date <- month.add(vdate, -since)}
  if (is.na(along)) {along_date <- dates[length(dates)]}
  else {along_date <- month.add(vdate, along)}
  if (sinceDay == 'first') {since_date <- month.firstday(since_date)}
  else if (sinceDay == 'last') {since_date <- month.lastday(since_date)}
  if (alongDay == 'first') {along_date <- month.firstday(along_date)}
  else if (alongDay == 'last') {along_date <- month.lastday(along_date)}
  return(subset.date(vdata=vdata, since_date, along_date, field=field))
}



subset.year <- function (vdata, vdate=NA, since=NA, along=NA, field=NA,
                          sinceDay='first', alongDay='last') {
  # Day in 'first', 'current', 'last'
  if (is.na(vdate)) {
    return(vdata)
  }
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  if (is.na(since)) {since_date <- dates[1]}
  else {since_date <- year.add(vdate, -since)}
  if (is.na(along)) {along_date <- dates[length(dates)]}
  else {along_date <- year.add(vdate, along)}
  if (sinceDay == 'first') {since_date <- year.firstday(since_date)}
  else if (sinceDay == 'last') {since_date <- year.lastday(since_date)}
  if (alongDay == 'first') {along_date <- year.firstday(along_date)}
  else if (alongDay == 'last') {along_date <- year.lastday(along_date)}
  return(subset.date(vdata, since_date, along_date, field))
}



# factor
extract.minimize <- function(vdata, baseZero=FALSE) {
  facts <- vdata - min(vdata)
  if (!baseZero) {
    facts <- facts + 1
  }
  return(facts)
}



extract.year <- function (vdata, field=NA, seqtype='none', baseZero=FALSE) {
  # seqtype in 'none', 'continius'
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  facts <- year(dates)
  if (seqtype == 'continius') {
    facts <- extract.minimize(facts, baseZero)
  }
  return(facts)
}



extract.month <- function (vdata, field=NA, seqtype='none', baseZero=FALSE) {
  # seqtype in 'none', 'continius', 'year'
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  if (seqtype == 'year') {
    facts <- extract.year(vdata, field, 'continius', baseZero)
  }
  else {
    facts <- month(dates)
    if (seqtype == 'continius') {
      facts <- extract.year(vdata, field, 'continius', TRUE) * 12 + facts
      facts <- extract.minimize(facts, baseZero)
    }
  } 
  return(facts)
}



extract.wday <- function (vdata, field=NA, seqtype='none', baseZero=FALSE) {
  # seqtype in 'none', 'continius', 'month', 'year', 'month_in_year'
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  facts <- wday(dates)
  if (seqtype == 'continius') {
    facts <- extract.month(vdata, field, 'continius', TRUE) * 7 + facts
    if (baseZero) {facts <- extract.minimize(facts, TRUE)}
  }
  else if (seqtype == 'month') {
    facts <- (extract.month(vdata, field) - 1) * 7 + facts
    if (baseZero) {facts <- extract.minimize(facts, TRUE)}
  }
  else if (seqtype == 'year') {
    facts <- extract.year(vdata, field, 'continius', TRUE) * 7 + facts
    if (baseZero) {facts <- extract.minimize(facts, TRUE)}
  }
  return(facts)
}



extract.fact <- function(vdata, field=NA, fields=c('year', 'month', 'wday'), 
                         by='none', seqyear='none', seqmonth='none', 
                         seqwday='none', baseZero=FALSE, asFactors=FALSE) {
  # fields is vector of 'wday', 'month', year'
  # by in 'none', month', year'
  if (!is.na(field)) {dates <- vdata[[field]]}
  else {dates <- vdata}
  fyear <- NULL
  fmonth <- NULL
  fwday <- NULL
  if (by == 'year') {
    if ('year' %in% fields) {
      fyear <- extract.year(vdata, field, seqyear, baseZero)
      if ('month' %in% fields) {
        fmonth <- extract.month(vdata, field, seqmonth, baseZero)
      }
      if ('wday' %in% fields) {
        fwday <- extract.wday(vdata, field, seqwday, baseZero)
      }
    }
    else {
      if ('month' %in% fields) {
        fmonth <- extract.month(vdata, field, 'year', baseZero)
        if ('wday' %in% fields) {
          fwday <- extract.wday(vdata, field, seqwday, baseZero)
        }
      }
      else if ('wday' %in% fields) {
        fwday <- extract.wday(vdata, field, 'year', baseZero)
      }
    }
  }

  else if (by == 'month') {
    if ('year' %in% fields) {
      fyear <- extract.year(vdata, field, seqyear, baseZero)
      if ('month' %in% fields) {
        fmonth <- extract.month(vdata, field)
        if ('wday' %in% fields) {
          fwday <- extract.wday(vdata, field, seqwday, baseZero)
        }
      }
      else if ('wday' %in% fields) {
        fwday <- extract.wday(vdata, field, 'month', baseZero)
      }
    }
    else if ('month' %in% fields) {
      fmonth <- extract.month(vdata, field, 'continius', baseZero)
      if ('wday' %in% fields) {
        fwday <- extract.wday(vdata, field)
      }
    }
    else if ('wday' %in% fields) {
      fwday <- extract.wday(vdata, field, 'continius')
    }
  }
  
  else if (by == 'none') {
    if ('year' %in% fields) {
      fyear <- extract.year(vdata, field, seqyear, baseZero)
    }
    if ('month' %in% fields) {
      fmonth <- extract.month(vdata, field, seqmonth, baseZero)
    }
    if ('wday' %in% fields) {
      fwday <- extract.wday(vdata, field, seqwday, baseZero)
    }
  } 
  if (is.na(field)) {field <- 'Date'}
  facts <- data.frame(dates)
  colnames(facts) <- c(as.name(field))
  if (!is.null(fyear)) {facts <- mutate(.data=facts, fyear=fyear)}
  if (!is.null(fmonth)) {facts <- mutate(.data=facts, fmonth=fmonth)}
  if (!is.null(fwday)) {facts <- facts <- mutate(.data=facts, fwday=fwday)}
  return(facts)
}



# aggregate
cnt.fact <- function(vdata, by) {
    # 
    cnts <- as.data.frame(count_(vdata, by))
    return(cnts)
}



aggr.fact <- function(vdata, fields, by, fun=sum, fieldDate=NULL) {
    #
    lby  <- list()
    for (field in by) {
        lby[[length(lby) + 1]] <- vdata[[field]]
    }
    aggrs <- aggregate(x=vdata[, fields], by=lby, FUN=fun, simplify=T)
    colnames(aggrs)  <- c(by, fields)
    if (identical(fun, median)) {
        cnts <- cnt.fact(vdata, by)
        aggrs <- inner_join(x=aggrs, y=cnts, by=by)
    }
    if (!is.null(fieldDate)) {
        dates <- aggregate(x=vdata[[fieldDate]], by=lby, FUN=max, simplify=T)
        colnames(dates) <- c(by, fieldDate)
        aggrs <- inner_join(x=aggrs, y=dates, by=by)
    }
    return(aggrs)
}



# na
na.interpolate <- function (vdata, neighbours=3, imp_var=FALSE, ...) {
  # 
  return(kNN(data=vdata, k=neighbours, imp_var=imp_var, ...))
}