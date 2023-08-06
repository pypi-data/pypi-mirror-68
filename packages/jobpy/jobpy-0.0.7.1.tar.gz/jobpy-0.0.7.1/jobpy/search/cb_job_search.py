from bs4 import BeautifulSoup
from jobpy.files.converter import csv_to_md, add_to_csv, remove_duplicate_rows

import requests
import datetime

job = 'software engineer'
location = 'Mechanicsburg, PA'


def grab_jobs_links(job_title: str, job_location: str):
    """
    Grabs the link for each job container and saves it to saved_jobs
    Removes the sign in link to avoid signing in to the CB page.
    :param job_title: str  desired job to be searched
    :param job_location: str  desired location to be searched
    :return: List of job links
    """
    web = requests.get(
        f"https://www.careerbuilder.com/jobs?keywords={job_title}&location={job_location}&sort=date_desc").text
    soup = BeautifulSoup(web, 'html.parser')

    # Career Builder sign in url. Used later to avoid signing in to grab the data.
    sign_in_url = "https://www.careerbuilder.com/user/sign-in?next="
    job_containers = soup.select('.data-results-content-parent')

    # Empty list used to store the values of the for loop below
    saved_jobs = []

    for idx, jobs in enumerate(job_containers):
        # CB requires the user to be signed in to see jobs. We use the replace method to bypass it.
        saved_jobs.append(f'{job_containers[idx].a.get("href", None).replace(sign_in_url, "")}')

    return saved_jobs


def get_job_information(url: str) -> object:
    """
    Uses bs4 to grab the information from each job container based on the url.
    :param url: str - career builder url of any job ("url")
    :return: A dictionary containing Job Name, Company Name, Job Location, Description, Skills and apply link.
    """
    website = requests.get(url).text
    job_soup = BeautifulSoup(website, 'html.parser')

    job_name = job_soup.select('.dib-m > h1')[0].getText()
    company_name = job_soup.select('.data-details > span:nth-child(1)')[0].getText()
    job_location = job_soup.select('.data-details > span:nth-child(2)')[0].getText()

    job_description = job_soup.select('#jdp_description > div.col-2 > div.col.big.col-mobile-full > p')
    job_description_2 = job_soup.select('#jdp_description > div:nth-child(1) > div:nth-child(1)')

    desc = []
    for idx, paragraph in enumerate(job_description):
        desc.append(job_description[idx].text)

    if len(desc) == 0:
        for idx, paragraph in enumerate(job_description_2):
            desc.append(job_description_2[idx].text)

    job_skills = []
    skills_container = job_soup.findAll("div", {"class": "check-bubble"})

    for idx, skill in enumerate(skills_container):
        job_skills.append(skills_container[idx].text)

    job_data = {'Job Title': job_name,
                'Company': company_name,
                'Location': job_location,
                'Description': desc,
                'Skills': job_skills,
                'Application Url': url}

    return job_data


# Loops through each link in saved_jobs and use the job_information function to add
# the data to a csv file. Counter is to create an id for the items in the csv file.
def start_search(job: str, location: str):
    """

    :param job: str Desired job title ("software engineer")
    :param location: str Desired job location ("Silicon Valley")
    :return:
    """
    for jobs in grab_jobs_links(job, location):
        add_to_csv(get_job_information(jobs), "software dev jobs")


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("Collecting jobs...")
    start_search(job, location)

    print("Removing duplicates")
    remove_duplicate_rows("panda_job_data.csv")

    print("Converting data...")
    csv_to_md("panda_job_data.csv", "tech jobs")

    print("Job collection completed")
    end_time = datetime.datetime.now()
    print(f"Time elapsed: {end_time - start_time}")
