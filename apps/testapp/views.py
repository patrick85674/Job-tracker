from datetime import datetime, timedelta
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.application.models.application import Application
from apps.job.models import Job
from apps.watchlist.models import Watchlist


def random_datetime(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )


start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 4, 30)

job_titles = [
    "Software Engineer", "Data Analyst", "UX Designer", "Product Manager",
    "DevOps Engineer", "Sales Manager", "Technical Writer",
    "Backend Developer", "Frontend Developer", "Marketing Specialist",
    "QA Engineer", "Full Stack Developer", "HR Coordinator",
    "Security Analyst", "Mobile Developer", "Project Manager", "AI Researcher",
    "Cloud Architect", "Business Analyst", "Support Engineer",
    "Content Strategist", "Systems Administrator", "Graphic Designer",
    "Network Engineer", "Recruiter", "Legal Counsel", "Financial Analyst",
    "E-commerce Manager", "Data Scientist", "Machine Learning Engineer",
    "Operations Manager", "SEO Specialist", "Technical Recruiter",
    "CRM Manager", "Video Editor", "Scrum Master", "UI Designer",
    "Social Media Manager", "Analytics Manager", "IT Support Specialist",
    "Technical Account Manager", "Business Development Rep",
    "Email Marketing Manager", "Data Engineer", "RPA Developer",
    "Cloud Engineer", "AI Engineer", "Compliance Officer",
    "Technical Project Manager", "Digital Strategist",
]

company_names = [
    "TechNova Solutions", "BlueWave Analytics", "CloudBridge Systems",
    "NextGen Innovations", "Quantum Leap Labs", "InspireSoft Inc.",
    "FusionCore Technologies", "BrightPath Group", "Nexis Digital",
    "Vertex Dynamics", "LumenEdge Technologies", "Pioneer AI",
    "Sparkline Ventures", "EchoSphere Media", "Visionary Creations",
    "CoreLogic Solutions", "MetaPeak Technologies", "ZenithWorks Inc.",
    "ElevateX Corporation", "Nimbus Technologies", "UrbanGrid Systems",
    "NovaLink Networks", "ShiftSpace Labs", "Ironclad Software",
    "ClearWave Data", "Skybound Robotics", "Radiant Pixel Studios",
    "OmniCloud Tech", "PulsePoint Group", "CodeForge Labs", "HyperNest AI",
    "BrightForge Inc.", "Elemental Designs", "Atlas Dynamics",
    "Synthetix Studios", "CloudCraft Innovations", "BeaconEdge Solutions",
    "Jetstream Systems", "Momentum Tech Group", "DigitalVista Inc.",
    "VoltEdge Systems", "CobaltSphere", "NimbleFox Technologies",
    "AuroraStack", "KineticHive Labs", "ForgeAhead Software",
    "ByteShift Systems", "AlphaStream Inc.", "Crestline Partners",
    "Lighthouse Innovations",
]
job_descriptions = [
    "Develop and maintain scalable web applications.",
    "Analyze large datasets to uncover business insights.",
    "Design user-centered interfaces and prototypes.",
    "Lead product development from concept to launch.",
    "Automate deployment pipelines and manage cloud infrastructure.",
    "Build backend APIs and integrate with third-party services.",
    "Create responsive front-end components using modern frameworks.",
    "Plan and execute digital marketing campaigns.",
    "Manage sales pipelines and build customer relationships.",
    "Write clear documentation for internal tools and APIs.",
    "Test software for bugs, performance, and usability issues.",
    "Develop full-stack solutions in a collaborative environment.",
    "Coordinate recruitment and onboarding processes.",
    "Identify and mitigate security vulnerabilities.",
    "Build native mobile applications for iOS and Android.",
    "Design scalable cloud architecture using AWS or Azure.",
    "Gather requirements and document business processes.",
    "Provide technical support to clients and internal teams.",
    "Oversee project timelines and team deliverables.",
    "Research and implement machine learning models.",
    "Write and edit content for marketing and social platforms.",
    "Manage company IT infrastructure and systems.",
    "Create visual assets for websites and social media.",
    "Monitor and optimize network performance.",
    "Source and evaluate potential job candidates.",
    "Manage online store operations and product listings.",
    "Build predictive models using statistical techniques.",
    "Deploy machine learning pipelines to production environments.",
    "Review contracts and provide legal guidance.",
    "Analyze financial statements and prepare reports.",
    "Ensure operational efficiency across departments.",
    "Optimize websites for search engine visibility.",
    "Identify and recruit top technical talent.",
    "Manage CRM tools and customer retention strategies.",
    "Edit and produce high-quality video content.",
    "Develop and manage social media strategies.",
    "Build dashboards and visualizations for business metrics.",
    "Provide tier-2 support and resolve escalated issues.",
    "Facilitate agile ceremonies and track team progress.",
    "Design wireframes and mockups for product features.",
    "Serve as the primary point of contact for enterprise clients.",
    "Generate leads and expand client base.",
    "Create, manage, and analyze email marketing campaigns.",
    "Build and manage scalable data pipelines.",
    "Deploy and maintain Kubernetes-based infrastructure.",
    "Implement AI-driven features for software applications.",
    "Ensure compliance with company policies and regulations.",
    "Oversee execution of cross-functional technology projects.",
    "Develop and refine online advertising strategies.",
    "Automate manual business processes using RPA tools."
]
locations = [
    "San Francisco, CA", "New York, NY", "Austin, TX", "Boston, MA",
    "Seattle, WA", "Chicago, IL", "Los Angeles, CA", "Miami, FL",
    "Denver, CO", "Portland, OR", "Atlanta, GA", "Remote", "Dallas, TX",
    "Phoenix, AZ", "San Diego, CA", "San Jose, CA", "Minneapolis, MN",
    "Tampa, FL", "Philadelphia, PA", "Cambridge, MA",
]

contact_names = [
    "Liam Johnson", "Emma Smith", "Noah Williams", "Olivia Brown",
    "Elijah Jones", "Ava Garcia", "James Miller", "Sophia Davis",
    "Benjamin Rodriguez", "Isabella Martinez", "Lucas Hernandez", "Mia Lopez",
    "Mason Gonzalez", "Charlotte Wilson", "Ethan Anderson", "Amelia Thomas",
    "Logan Taylor", "Harper Moore", "Jackson Jackson", "Evelyn Martin",
    "Alexander Lee", "Abigail Perez", "Sebastian Thompson", "Ella White",
    "Aiden Harris", "Scarlett Sanchez", "Matthew Clark", "Emily Ramirez",
    "Henry Lewis", "Elizabeth Robinson", "Joseph Walker", "Luna Hall",
    "Samuel Young", "Sofia Allen", "David King", "Chloe Wright", "Wyatt Scott",
    "Grace Green", "Owen Adams", "Victoria Baker", "John Nelson",
    "Penelope Hill", "Julian Rivera", "Layla Campbell", "Levi Mitchell",
    "Nora Roberts", "Daniel Carter", "Zoey Phillips", "Gabriel Evans",
    "Hannah Turner",
]
comments = [
    "Great experience with relevant skills.",
    "Candidate needs to improve communication.",
    "Strong portfolio, especially the last project.",
    "Not a good fit for the current team structure.",
    "Excellent interview, very confident.",
    "Resume lacks detail on previous roles.",
    "Follow-up needed on salary expectations.",
    "Technical skills are above average.",
    "Needs more leadership experience.",
    "Follow-up call scheduled for next week.",
    "Candidate has potential, consider for other roles.",
    "Impressive education background.",
    "Waiting on reference check results.",
    "Soft skills need improvement.",
    "Highly recommended by former manager.",
    "Overqualified for this position.",
    "Asked insightful questions during the interview.",
    "Cultural fit may be a concern.",
    "Requested remote work flexibility.",
    "Needs to complete the coding test.",
    "Great attitude and willingness to learn.",
    "Declined offer due to compensation.",
    "Rescheduled interview twice — a concern.",
    "Very responsive and professional.",
    "Application missing cover letter.",
    "Preferred by the hiring manager.",
    "Limited experience with required tools.",
    "Strong fit for junior developer role.",
    "Good communication but lacking experience.",
    "Excellent presentation skills.",
    "Still pursuing other opportunities.",
    "Followed up promptly after interview.",
    "References were very positive.",
    "Availability to start is immediate.",
    "Needs to improve technical depth.",
    "Not interested in relocation.",
    "Referred by internal employee.",
    "Very interested in the role and company.",
    "Good problem-solving demonstration.",
    "Needs further screening for technical fit.",
    "Currently employed, 2-week notice required.",
    "Looking for part-time opportunity only.",
    "Has worked with similar clients before.",
    "Lacks relevant industry experience.",
    "Candidate withdrew application.",
    "Might be better suited for future openings.",
    "Requested feedback after rejection.",
    "Willing to relocate if required.",
    "Well-prepared for the interview.",
    "No-show for first interview — rescheduled.",
    "Resume is outdated but interview was strong.",
]
phone_numbers = [
    "+1-202-555-0136", "+44 20 7946 0958", "+91-9876543210",
    "+49-1512-3456789", "+81-90-1234-5678", "+33 6 12 34 56 78",
    "+61-412-345-678", "+55 11 91234-5678", "+86 139 1234 5678",
    "+34 612 34 56 78", "+7 916 123-45-67", "+39 347 123 4567",
    "+27 82 123 4567", "+82 10-1234-5678", "+46 70 123 45 67",
    "+971 50 123 4567", "+64 21 123 4567", "+351 91 234 5678",
    "+31 6 12345678", "+41 79 123 45 67", "+48 512 345 678",
    "+62 812-3456-7890", "+234 803 123 4567", "+66 081 234 5678",
    "+998 90 123 45 67", "+20 100 123 4567", "+63 917 123 4567",
    "+90 532 123 4567", "+961 3 123 456", "+421 915 123 456",
    "+52 1 55 1234 5678", "+370 612 34 567", "+1-647-555-0199",
    "+353 87 123 4567", "+43 660 1234567", "+94 71 234 5678",
    "+45 20 12 34 56", "+86 138 0013 8000", "+385 91 123 4567",
    "+358 50 1234567", "+1-408-555-0193", "+47 412 34 567",
    "+48 789 456 123", "+60 12-345 6789", "+994 50 123 45 67",
    "+84 912 345 678", "+966 50 123 4567", "+977 980-1234567",
    "+1-876-555-1234", "+66 91 234 5678",
]


@login_required
def add_sample_data_view(request):

    for i in range(50):
        created_at = random_datetime(start_date, end_date)
        updated_at = created_at + timedelta(days=random.randint(0, 365))
        job_name = job_titles[i]
        company_name = company_names[i]
        location = random.choice(locations)
        link = f"https://example.com/job/{i+1}"
        job_description = job_descriptions[i]

        contact_name = contact_names[i]
        contact_email = f"user{i+1}@example.com"
        contact_phone = phone_numbers[i]
        comment = comments[i]
        status = random.choice(Application.StatusType.choices)[0]
        platform = random.choice(Application.PlatformType.choices)[0]

        job = Job.objects.create(
            user=request.user,
            job_name=job_name,
            link=link,
            job_description=job_description,
            company_name=company_name,
            location=location,
            created_at=created_at,
            updated_at=updated_at,
        )
        Application.objects.create(
            user=request.user,
            job=job,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            status=status,
            platform=platform,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at,
        )
        Watchlist.objects.create(
            user=request.user,
            job=job,
            created_at=created_at,
            updated_at=updated_at,
        )

    return HttpResponse(
        f"Added sample data ({i+1} jobs, applications and watchlist elements)!"
    )
