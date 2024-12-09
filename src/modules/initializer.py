from src.modules import crawler,file_mapper
import schedule
import time
from conf.configurator import is_scheduler_enabled

def init_search_engine():
    file_mapper.generate_file_map()
    crawler.main()

def main():
    init_search_engine()
    print ("Seach Engine is initialized...")
    
    if (is_scheduler_enabled()):
        # Schedule weekly crawling
        schedule.every().week.do(init_search_engine)
        print ("Seach Engine Initializer is scheduled to execute weekly...")

        # Keep the script running to honor the schedule
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print ("Seach Engine Initializer scheduling is deactivated...")

if __name__ == "__main__":
    main()


