from supabase import create_client

SUPABASE_URL = "https://gpveapezfludfcedvbhp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdwdmVhcGV6Zmx1ZGZjZWR2YmhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNTk4NTQsImV4cCI6MjA4ODczNTg1NH0.FpIcgI_H4GcNScAqhCWvI_bkPSEcb8i_7r3Q01rqdMg"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def add_memory(role, content):

    supabase.table("message").insert({
        "role": role,
        "content": content
    }).execute()


def get_memory():

    response = supabase.table("message").select("*").execute()

    messages = []

    for row in response.data:
        messages.append({
            "role": row["role"],
            "content": row["content"]
        })

    return messages