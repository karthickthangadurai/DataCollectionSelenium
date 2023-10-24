# =====================================Linkedin Scrapping Functions========================================#
def linkedin_login(email, password):  # returning the driver and no of pages. 1st Execution
    # Driver path
    driver = webdriver.Chrome()

    # Maximize Window
    driver.maximize_window()
    driver.minimize_window()
    driver.maximize_window()
    driver.switch_to.window(driver.current_window_handle)
    driver.implicitly_wait(10)

    # Enter to the site
    driver.get('https://www.linkedin.com/login');
    time.sleep(2)

    # ==============================finding the elements of username & password and sign in=======================#
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    time.sleep(1)
    # Login button
    driver.find_element(By.XPATH, "//button[@aria-label='Sign in']").click()
    driver.implicitly_wait(10)

    return driver


def fill_job_location(driver, position, location):  # fill the jobs and position. 2nd Execution
    # =======================filter Past week, Entry level, Internship Job opportunities=========================#
    # ====================================going to the Jobs page==================================================#
    driver.get('https://www.linkedin.com/jobs/search')
    # waiting load
    time.sleep(2)

    # Go to search results directly
    # ==============fill job title, clearing the location placeholder and fill location and submit================#
    driver.find_element(By.XPATH, '//*[@aria-label="Search by title, skill, or company"]').send_keys(position)
    driver.find_element(By.XPATH, '//*[@aria-label="City, state, or zip code"]').clear()
    driver.find_element(By.XPATH, '//*[@aria-label="City, state, or zip code"]').send_keys(location)
    driver.find_element(By.CLASS_NAME, 'jobs-search-box__submit-button').click()
    time.sleep(30)

    # =============================clicking the date posted buttons and selecting past week=========================#
    date_posted_xpath = "//button[@aria-label='Date posted filter. Clicking this button displays all Date posted filter options.']"
    driver.find_element(By.XPATH, date_posted_xpath).click()
    time.sleep(30)
    driver.find_element(By.XPATH, "//span[text()='Past week']").click()
    # =======show results button - multiple show results buttons present - taking the 1st search button for now========#
    list_date_modified = driver.find_elements(By.CSS_SELECTOR,
                                              'div.reusable-search-filters-buttons>button:nth-child(2)>span')
    list_date_modified[0].click()
    time.sleep(10)

    # ==============all buttons in the options - jobs, date posted, experience level, company, on-site remote==============#
    all_buttons = driver.find_elements(By.CSS_SELECTOR, "button.artdeco-pill:nth-child(1)")
    # took all the buttons and selected the 3rd one for experience level

    # =====click the experience level and click on entry level, internship and click on show results buttons============#
    all_buttons[2].click()  # clicking the experience level button
    time.sleep(20)
    driver.find_element(By.XPATH, "//span[text()='Internship']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//span[text()='Entry level']").click()
    time.sleep(3)
    # show results button - multiple show results buttons present - taking the 2nd search button for now
    list_date_modified = driver.find_elements(By.CSS_SELECTOR,
                                              'div.reusable-search-filters-buttons>button:nth-child(2)>span')
    list_date_modified[1].click()
    time.sleep(10)

    # ==========================getting the total results to calculate the no of pages================================#
    total_results_text = driver.find_element(By.CSS_SELECTOR, 'div.jobs-search-results-list__subtitle').text
    print(total_results_text)
    total_results = int("".join(re.findall(r'\d+', total_results_text)))

    # =======================================calculating the no of pages===============================================#
    total_pages = math.ceil(int(total_results) / 25)
    print(total_pages)

    return driver, total_pages  # returning driver and total pages


def collect_links(driver, total_pages):  # giving driver and total pages as input 3rd Execution

    # ========================Navigate all pages and collecting all links=============================================#
    print('Links are being collected now. So go and minimize the screen to collect all links')
    # =========================screen has to minimized here===============================================#
    links = []
    try:
        # ========================going to the Jobs page==================================================#
        for page in range(2, total_pages + 1):
            time.sleep(2)
            # ==========================identify and get entire jobs links block=================#
            jobs_block = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')

            # ============================get all job linkselements==============================#
            jobs_list = jobs_block.find_elements(By.CLASS_NAME, 'job-card-list__entity-lockup')

            for i in jobs_list:
                driver.execute_script("arguments[0].scrollIntoView();", i)
                time.sleep(2)
                # print(jobs_list)
                jobs_block = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
                jobs_list = jobs_block.find_elements(By.CLASS_NAME, 'job-card-list__entity-lockup')

            # ==========================identify and get entire jobs links block=================#
            # ============================get all job links elements==============================#
            jobs_block = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
            jobs_list = jobs_block.find_elements(By.CLASS_NAME, 'job-card-list__entity-lockup')

            # print(jobs_block.find_elements(By.XPATH,all_links_xpath))
            # =====================collect the links one by one===================================#
            for job in jobs_list:
                all_links = job.find_elements(By.TAG_NAME, 'a')
                # print(all_links)
                for a in all_links:
                    if str(a.get_attribute('href')).startswith(
                            "https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links:
                        links.append(a.get_attribute('href'))
                    else:
                        pass
                # scroll down for each job element
                driver.execute_script("arguments[0].scrollIntoView();", job)
                driver.implicitly_wait(10)

            # ==========================going to the next page and printing the current time=============#
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            print(f'Collecting the links in the page: {page - 1}', "Current Time is :", curr_time)

            # ==========================going to 8th page and giving refresh=============================#
            if page == 8:
                driver.refresh()
                time.sleep(20)
            # ===================find the next page element and click to next page=======================#
            driver.find_element(By.XPATH, f"//button[@aria-label='Page {page}']").click()
            time.sleep(3)
    except:

        pass

    driver.close()
    return links  # return all the collected links


def jobdictbase():
    Job_Overall_Details = {"job_titles": [], "contact_person": [], "contact_team": [], "company_name": [],
                           "company_link": [], "location_name": [], "employment_type": [], "seniority_level": [],
                           "post_date": [], "applicants_count": [], "description": [], "job_links": []}

    return Job_Overall_Details


def waitpoint():

    wait_point = 1
    
    return wait_point


def jobdetailedscraper(links, Job_Overall_Details, wait_point):  # giving links and overall details dict and wait point

    """Joboveralldetailsdict = {"job_titles":[],"contact_person":[],"contact_team":[],"company_name":[],"company_link": [],
                       "location_name":[],"employment_type": [],"seniority_level":[],"post_date":[],
                       "applicants_count":[],"description":[],"job_links":[]}"""

    # ==============================collecting the details of each job===========================================#
    for link in links:
        # ======================checking if the job is already scrapped=========================================#
        if link not in Job_Overall_Details["job_links"]:
            # ==============================creating the chrome driver===========================================#
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            driver = webdriver.Chrome(options=op)
            # driver = webdriver.Chrome()
            driver.get(link)
            driver.maximize_window()
            time.sleep(2)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(1)
            # =============================clicking the show more button=========================================#
            driver.find_element(By.CLASS_NAME, "show-more-less-html__button").click()
            # =============================getting the top card job details==========================================#
            top_card = driver.find_element(By.CLASS_NAME, 'top-card-layout__card')

            # =============================getting the all job details===============================================#

            Job_Overall_Details["job_titles"].append(top_card.find_element(By.TAG_NAME, 'h1').text)

            # =====================trying to fetch the contact person and contact team if available==================#
            try:
                person = driver.find_element(By.CSS_SELECTOR, "div.message-the-recruiter>div>div>h3").text
                team = driver.find_element(By.CSS_SELECTOR, "div.message-the-recruiter>div>div>h4").text
                # print(person, team)
                Job_Overall_Details["contact_person"].append(person)
                Job_Overall_Details["contact_team"].append(team)
            except:
                Job_Overall_Details["contact_person"].append('')
                Job_Overall_Details["contact_team"].append('')

            # =============================getting the company details===============================================#
            Job_Overall_Details["company_name"].append(
                top_card.find_element(By.CSS_SELECTOR, 'div.top-card-layout__entity-info>h4>div>span').text)
            Job_Overall_Details["company_link"].append(top_card.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            Job_Overall_Details["location_name"].append(top_card.find_element(By.CSS_SELECTOR,
                                                                              'div.top-card-layout__entity-info>h4>div>span.topcard__flavor--bullet').text)

            # =============================getting the post date and applicant count=================================#
            Job_Overall_Details["post_date"].append(top_card.find_element(By.CLASS_NAME, 'posted-time-ago__text').text)
            Job_Overall_Details["applicants_count"].append(
                top_card.find_element(By.CLASS_NAME, 'num-applicants__caption').text)

            # =============================getting the seniority level and employment type============================#
            job_criteria_text_list = [i.text for i in
                                      driver.find_elements(By.CSS_SELECTOR, "span.description__job-criteria-text")]

            # employment type
            if len(job_criteria_text_list) >= 2:
                Job_Overall_Details["employment_type"].append(job_criteria_text_list[1])
            else:
                Job_Overall_Details["employment_type"].append('None')

            Job_Overall_Details["seniority_level"].append(job_criteria_text_list[0])

            # =============================getting the job description and job links==================================#
            # print(driver.find_element(By.CLASS_NAME,'description__text').text)
            Job_Overall_Details["description"].append(driver.find_element(By.CLASS_NAME, 'description__text').text)
            Job_Overall_Details["job_links"].append(link)

            # ===================================closing the driver==================================================#
            driver.close()

            wait_point += 1
            # =================================if 15 jobs scrapped then sleep for 10 sec===========================#
            if wait_point % 15 == 0:
                # using now() to get current time
                current_time = time.strftime("%H:%M:%S", time.localtime())
                print(f"{wait_point} links completed", " The current time in india is :", current_time)
                time.sleep(10)

        else:

            pass

    return Job_Overall_Details #returns scraped jobs dictionary


# driver = linkedin_login(email, password)
# JobPageDriverCount = fill_job_location(driver, position, location)
# links = collect_links(JobPageDriverCount[0], JobPageDriverCount[1])

# JobScrapperReturn = jobdetailedscraper(links, jobdictbase(), waitpoint())
# df = pd.DataFrame(JobScrapperReturn)
# print(df.head())
