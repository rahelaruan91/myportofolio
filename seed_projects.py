from main.models import Project

Project.objects.all().delete()

Project.objects.create(
    title="MediVoice",
    subheading="Accessibility-First Medication Platform for Elderly",
    description="A voice-first medication companion that helps elderly users manage their daily medications more safely and independently, addressing challenges caused by memory decline, visual limitations, and complex medication routines.",
    thumbnail="img/medivoice-preview.png",
    project_url="https://www.figma.com/proto/HobETRCZ1a2cr1XwRcvzRM/MediVoice---Gemastik-UX?node-id=15637-3102&t=flmPqdfgXW1p2yUM-1&scaling=scale-down&content-scaling=fixed&page-id=15637%3A2726",
)

Project.objects.create(
    title="SehaTri",
    subheading="Smart Primary Puskesmas Queue & Triage Platform",
    description="A digital queue and triage platform that makes primary healthcare visits more predictable by allowing patients to register remotely, monitor estimated waiting times, and understand their position in the service journey.",
    thumbnail="img/sehatri-preview.png",
    project_url="https://www.figma.com/proto/nq0zFtJ2teNZsWvJuxLN3U/SehaTri?node-id=13829-18029&p=f&t=e8HWrOXZJBdZdcIb-1&scaling=min-zoom&content-scaling=fixed&page-id=13100%3A11378",
)

Project.objects.create(
    title="FisioMate",
    subheading="AI-Powered Remote Therapeutic Monitoring",
    description="An AI-powered post-rehabilitation platform that connects patients and physiotherapists throughout the recovery journey, supporting consistent exercise routines and personalized rehabilitation programs beyond clinical settings.",
    thumbnail="img/fisiomate-preview.png",
    project_url="https://www.figma.com/proto/IseKhbUw1LH8HakQbzwtVu/FisioMate?node-id=13019-49185&p=f&t=P2GWIZwHcJiq7vI5-1&scaling=min-zoom&content-scaling=fixed&page-id=4004%3A15&starting-point-node-id=13019%3A49185",
)

Project.objects.create(
    title="Werra",
    subheading="Circular Thrift E-Commerce Platform",
    description="An AI-powered secondhand fashion marketplace that helps users discover and evaluate pre-owned clothing through AI-assisted garment detection, making thrift shopping more transparent and convenient.",
    thumbnail="img/werra-preview.png",
    project_url="https://www.figma.com/proto/L1axQDs1dfD62MH5fCs9mn/werra?node-id=781-9678&p=f&t=zmQ8EQZHjAat3LWt-1&scaling=scale-down&content-scaling=fixed&page-id=761%3A8294&starting-point-node-id=781%3A9678&show-proto-sidebar=1",
)

Project.objects.create(
    title="MuseumKu",
    subheading="Cultural Exploration & Engagement Platform",
    description="A digital cultural exploration platform that transforms traditional museum visits into interactive and personalized journeys, helping younger audiences discover and engage with cultural heritage in a more relevant way.",
    thumbnail="img/museumku-preview.png",
    project_url="https://www.figma.com/proto/96zD34uBELNo5LrQjlqNV1/MuseumKu---Budaya-Go?node-id=2091-1853&p=f&t=PVYSMdG890NDgnlu-1&scaling=scale-down&content-scaling=fixed&page-id=250%3A510&starting-point-node-id=2079%3A2127",
)

print(f"Berhasil, total project sekarang: {Project.objects.count()}")