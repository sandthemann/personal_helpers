from datetime import datetime, timedelta
import pytz

class TimingError(Exception):
    """A custom exception used to report errors in use of Timing class"""

class Timing:
    """
        Used to set initial values and date within the Timing Class
          
        attributes:
          -today: todays date
          -date_change: todays date plus or minus number of days
          -start: time to start measuring timing
          -lap: time from previous measurement
          -stop: stop timing
          -get_times: dictionary of times collected
          -diff: difference between start and stop time
          -update_email: send an update email
    """
    
    
    def __init__(self, timezone = 'America/Ohio'):
      if timezone:
        today = datetime.now(pytz.timezone('America/Ohio'))
      else:
        today = datetime.now()
      self._start_time = None
      self._end_time = None
      self._diff = None
      self._today = today
        
        
    def today(self, as_string = True):
      """
      Get todays date
      """
      if as_string:
         today = self._today.strftime("%Y-%m-%d")
      return today
        
      
    def date_change(self, day_change = 0, as_string = True):
      """
        Used to get a date that is greater than or less than the current date
      
        args:
          -day_change (default = 0): how many days to go forward or backwards (Ex. -1 would return yesterday, 1 would return tomorrow) (int)
        output:
          -Date
      """
      self._assertion(isinstance(day_change, int), TypeError, f'day change value should be an integer type, you provided {day_change}')
      new_day = self._today - timedelta(days = -1*int(day_change))
      if as_string:
         new_day = new_day.strftime("%Y-%m-%d")
      return new_day

    
    def start(self):
        """
        Start a new timer
        """
        if self._start_time is not None:
            raise TimingError(f"Timer is running. Use .stop() to stop it")

        self._start_time = datetime.now()
        self._end_time = None
        self._lap_count = 0
        self._times = {}
        self._times['start'] = {}
        self._times['start']['time'] = self._start_time
        
        
    def lap(self, name = None):
        """
        Get time differences between different periods
        """
        if self._start_time is None:
            raise TimingError(f"Timer is not running. Use .start() to start it")
        if self._end_time is not None:
            raise TimingError(f"Timer is not running. Use .start() to start it")
        self._assertion(isinstance(name, (str, type(None))), TypeError, f'lap name should be a string, you provided {type(name)}')
        lap_time = datetime.now()
        last_time = list(self._times.values())[-1]['time']
        self._lap_count += 1
        if name is None:
          name = self._lap_count
        self._times[name] = {}
        self._times[name]['time'] = lap_time 
        if self._lap_count == 1:
          self._times[name]['diff'] = lap_time - last_time
          print(f"Elapsed time for {name} since start: {self._times[name]['diff']}")
        else:
          self._times[name]['diff'] = lap_time - last_time
          print(f"Elapsed time for {name} from lap {list(self._times.keys())[-1]}: {self._times[name]['diff']}")
        return lap_time
      
      
    def stop(self):
        """
        Stop the timer, and report the elapsed time
        """
        if self._start_time is None:
            raise TimingError(f"Timer is not running. Use .start() to start it")
      
        self._end_time = datetime.now()
        self._diff = self._end_time - self._start_time
        self._start_time = None
        self._times['stop'] = {}
        self._times['stop']['time'] = self._end_time
        self._times['stop']['diff'] = self._end_time - list(self._times.values())[-1]['time']
        self._times['total_diff'] = self._diff
        print(f"Elapsed time: {self._diff}")
        
        
    def get_times(self):
        """
        Get a dictionary of all start, lap, and stop times for the current timing period
        """
        if self._times == {}:
            raise TimingError(f"No times have been recorded. Use .start() to start the timer and .lap() to log laps")
        print(self._times)
        return self._times
      
      
    def diff(self):
        """Report the elapsed time from start to finish"""
        if self._diff is None:
            raise TimingError(f"No difference has been logged at this time. Use .start() and .stop() to utilize timer")
        print(self._diff)
        return self._diff