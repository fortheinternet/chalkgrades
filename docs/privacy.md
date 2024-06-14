# Privacy Policy

Let's get to the point. **Chalk is public domain open-source software that anyone (even you) can download, run, and host easily.** The maintainers, developers, and contributors (here and foremost referred to as "Maintainers") do not have access to any information you enter, anywhere.

**That information is accessible only to your school's IT personnel** (here and foremost referred to as "Administrator(s)"), who is/are managing the database. If you're running Chalk on Vercel, then you can check the environment variables in the Settings tab. If you're running it locally or self-hosting it (based asf btw), you can see values in the ```.env``` file of project_root/api/.

These values are important because they provide important project settings, **such as what database to connect to.** This is where all your data goes - and the Chalk codebase is designed to work well with [Supabase.](https://supabase.com)

If you are using Vercel, I recommend their Privacy Policy over yonder: [Privacy Policy - Vercel](https://vercel.com/legal/privacy-policy)

And Supabase's policies: [Privacy Policy | Supabase](https://supabase.com/privacy)

## Who has access to my data?

1. Your school's administrator
2. You also have access :D
3. I don't have access

## Where is my data?

Your data is believed to be hosted on an AWS datacenter, somewhere that is the closest to you, operated by Supabase, and accessible by whoever is operating the DB (your school it admin :D).

If you're using the servive from Hungary, the closest datacenter is in *Frankfurt, Germany.* Again, this could differ school-to-school, but setting it up there makes sense because of latency issues.

## What can I do to delete, access, or modify my data?

You can contact your school.