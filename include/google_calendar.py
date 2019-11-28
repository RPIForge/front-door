from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
import pickle


class calendar:
    #accessing variables
    running = False
    
    #calendar variables
    calendar_id=None
    calendar_service = None
    
    #names
    minute_identities = ['min','mins','minutes','minute']
    hour_identities = ['hour','hours']
    second_identities = ['sec','seconds','secs','second']
    
    def __init__(self):
            print("initalizing calendar")
            #Load credentials from file
            credentials = pickle.load(open("include/credentials/token.pkl", "rb"))
    
            #get the calendar id
            self.calendar_service = build("calendar", "v3", credentials=credentials)
            
            result = self.calendar_service.calendarList().list().execute()
            result_element=0
            for calendar in result['items']:
                if(calendar['summary']=='Volunteer Hours'):
                    break
                result_element=result_element+1
                
            self.calendar_id = result['items'][result_element]['id']
            print("finished initalization")    
    
    
    
    
    
    
    
    
    
    ####################### SET EVENT FUNCTIONS #####################################
    def get_user_events(self, user):
        upcoming_events = self.calendar_service.events().list(calendarId=self.calendar_id,timeMin=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")).execute()
        matching_events=[]
        for event in upcoming_events['items']:
            if(event['status']=='cancelled'):
                continue  
            if(str(event['summary']).lower()==user):
                if ('recurrence' in event):
                    recurring_events_list = self.calendar_service.events().instances(calendarId=self.calendar_id,eventId=event['id'],showDeleted=True, timeMin=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")).execute()
                    
                    for recurring_event in recurring_events_list['items']:
                        if(recurring_event['status']=='cancelled'):
                            continue  
                        if(str(recurring_event['summary']).lower()==user):
                            matching_events.append(recurring_event)
                else:
                    matching_events.append(event)
        
        return matching_events
    
    def get_next_user_event(self, user):
        user_events = self.get_user_events(user)
        current_time = datetime.datetime.now()
        next_event={'event':{},'start_time':datetime.datetime(2040,1,1)}
        for event in user_events:
            if 'dateTime' in event['start']:
                event_time = datetime.datetime.strptime(event['start']['dateTime'][:16],'%Y-%m-%dT%H:%M')
                                
                if(current_time <= event_time <= next_event['start_time']):
                    next_event['event']=event
                    next_event['start_time']=event_time
        return next_event['event']
        
    
    ###################### GET CURRENT EVENT FUNCTIONS ############################### 
    def search_reocurring_events(self, events,current_time):
        results=[]
        for event in events['items']:
            if(event['status']=='cancelled'):
                continue  
            if 'dateTime' in event['start']:
                #get the events hours
                start_hour = datetime.datetime.strptime(event['start']['dateTime'][11:16],'%H:%M')
                end_hour = datetime.datetime.strptime(event['end']['dateTime'][11:16],'%H:%M')
        
                #set the day to today
                start_time = start_hour.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                end_time = end_hour.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                
                #see if current time is between hours
                
                if(start_time.time() <= current_time.time() <= end_time.time()):
                    if(event['summary']=='Volunteer Hours'):
                        continue
                    #append result to list
                    results.append(event['summary'])
        return results 
        
        
    #search for events within the current time
    def search_events(self, events,current_time):
        results=[]
        list_id=[]
        for event in events['items']:
            if(event['status']=='cancelled'):
                continue  
            if 'dateTime' in event['start']:
                #get the events hours
                start_hour = datetime.datetime.strptime(event['start']['dateTime'][11:16],'%H:%M')
                end_hour = datetime.datetime.strptime(event['end']['dateTime'][11:16],'%H:%M')
        
                #set the day to today
                start_time = start_hour.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                end_time = end_hour.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                
                #see if current time is between hours
                event_result = {}
                if(start_time.time() <= current_time.time() <= end_time.time()):
                    if(event['summary']=='Volunteer Hours'):
                        continue
                    if(event['id'] in list_id):
                        continue
                    #get all of the recurring events
                    start_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_day = current_time.replace(hour=23, minute=59, second=0, microsecond=0)

                    if ('recurrence' in event):
                        recurring_events_list = self.calendar_service.events().instances(calendarId=self.calendar_id,eventId=event['id'],showDeleted=True, timeMin=start_day.strftime("%Y-%m-%dT%H:%M:%SZ"),timeMax=end_day.strftime("%Y-%m-%dT%H:%M:%SZ")).execute()
                        
                        current_recurring_events = self.search_reocurring_events(recurring_events_list,current_time)
                        
                        for actual_events in current_recurring_events:
                            #append result to list
                            event_result['name']=event['summary']
                            event_result['id']=actual_events
                            event_result['start_time']=start_time.time()
                            event_result['end_time']=end_time.time()
                            results.append(event_result)
                    else:
                        event_result['name']=event['summary']
                        event_result['id']=event['id']
                        event_result['start_time']=start_time.time()
                        event_result['end_time']=end_time.time()
                        results.append(event_result)
        return results 
    
    def get_current_events(self):
        #get current time and the begenning/end of today
        current_time = datetime.datetime.now()
        start_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = current_time.replace(hour=23, minute=59, second=0, microsecond=0)


        try:
            #get all events today
            events = self.calendar_service.events().list(calendarId=self.calendar_id,timeMin=start_day.strftime("%Y-%m-%dT%H:%M:%SZ"),timeMax=end_day.strftime("%Y-%m-%dT%H:%M:%SZ")).execute()
        
            #get all of the events happening right now
            current_events = self.search_events(events,current_time)
        except:
            
            raise Exception('Unable to get data')
            current_events=[]
        
        return current_events
    
    ################################ UPDATE EVENT FUNCTIONS ########################################
    def update_event(self, event):
        self.calendar_service.events().update(calendarId=self.calendar_id,eventId=event['id'],body=event).execute()
        
    def cancel_hours(self,user):
        next_event = self.get_next_user_event(user)
        try:
            next_event['status']='cancelled'
            self.update_event(next_event)
            return True
        except:
            return False
            
    
    def change_hours(self,user,hour_name,hour_value):
        next_event = self.get_next_user_event(user)
        
        tag = next_event['start']['dateTime'][19:]
        event_time = datetime.datetime.strptime(next_event['start']['dateTime'][:18],'%Y-%m-%dT%H:%M:%S')
        event_end_time = datetime.datetime.strptime(next_event['end']['dateTime'][:18],'%Y-%m-%dT%H:%M:%S')
        #get new start time
        
        new_event_time=event_time
        
        if(hour_name in self.second_identities):
            new_event_time = event_time + datetime.timedelta(seconds=hour_value)
        elif(hour_name in self.minute_identities):
            new_event_time =  event_time + datetime.timedelta(minutes=hour_value)
        elif(hour_name in self.hour_identities):
            new_event_time  = event_time + datetime.timedelta(hours=hour_value)
        
        if(new_event_time>event_end_time):
            return False
        
        changed_event = next_event
        
        changed_event['start']['dateTime'] = new_event_time.strftime('%Y-%m-%dT%H:%M:%S')+tag
        
        print(changed_event)
        try:
            self.update_event(changed_event)
            return True
        except:
            return False
    
calendar()
