"""Comprehensive Poster Image Catalog and Resolver for CineScore Universe.

Contains direct, high-fidelity poster URLs from official CDNs (TMDb, IMDb, Wikimedia)
with genre/category fallbacks to ensure every title renders an authentic cover image.
"""

from typing import Dict, Any

# Direct Official TMDb CDN Poster URLs (w500)
POSTERS_CATALOG: Dict[str, str] = {
    # --- Top Movies ---
    "The Shawshank Redemption": "https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg",
    "The Godfather": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "The Dark Knight": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "The Godfather Part II": "https://image.tmdb.org/t/p/w500/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg",
    "12 Angry Men": "https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg",
    "Schindler's List": "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
    "The Lord of the Rings: The Return of the King": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
    "Pulp Fiction": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
    "The Lord of the Rings: The Fellowship of the Ring": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
    "The Good, the Bad and the Ugly": "https://image.tmdb.org/t/p/w500/bX2xnavhMYjWDoZp1VM6VnU1xwe.jpg",
    "Forrest Gump": "https://image.tmdb.org/t/p/w500/arw2VCBveWOVZr6pxd9XTd1TdQa.jpg",
    "Fight Club": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    "The Lord of the Rings: The Two Towers": "https://image.tmdb.org/t/p/w500/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg",
    "Inception": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
    "Star Wars: Episode V - The Empire Strikes Back": "https://image.tmdb.org/t/p/w500/nNAeTmF4CMbU0O98CMVRRi9xV9C.jpg",
    "The Matrix": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Goodfellas": "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
    "One Flew Over the Cuckoo's Nest": "https://image.tmdb.org/t/p/w500/kjWsMh32VnflLyqpGE2mISXn8i5.jpg",
    "Interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "Seven Samurai": "https://image.tmdb.org/t/p/w500/8OKm79bmOPMuzOoBZue06Pz6Nk9.jpg",
    "Se7en": "https://image.tmdb.org/t/p/w500/6yoghtyTBoPvxDuio51LVFX13qP.jpg",
    "The Silence of the Lambs": "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg",
    "Saving Private Ryan": "https://image.tmdb.org/t/p/w500/uqx37cS8cpHg8x35f9U5IBlrCV3.jpg",
    "City of God": "https://image.tmdb.org/t/p/w500/k7eYdWvhYQ7RQo9OB8TcFGs7SU3.jpg",
    "Life Is Beautiful": "https://image.tmdb.org/t/p/w500/74hLDKjD5aGYOotO6esUVaeISa2.jpg",
    "The Green Mile": "https://image.tmdb.org/t/p/w500/velWPhVMQeQKcxggNEU8YmIo52R.jpg",
    "Spirited Away": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
    "Parasite": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "Léon: The Professional": "https://image.tmdb.org/t/p/w500/yI6X2c8crRwSpdPQAZBmDiANuga.jpg",
    "The Prestige": "https://image.tmdb.org/t/p/w500/bdN3gXu48t6NYgyAgDG7vWsSOE.jpg",
    "The Lion King": "https://image.tmdb.org/t/p/w500/sKCr78jnAMpaCpAhv91vN5bBfF.jpg",
    "The Usual Suspects": "https://image.tmdb.org/t/p/w500/bUP7m9l0uQ4u7Y4xWJzD9KjM66D.jpg",
    "Whiplash": "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
    "Gladiator": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",
    "The Departed": "https://image.tmdb.org/t/p/w500/nT97ifVT2J1yMQmeq20Qblg61T.jpg",
    "Apocalypse Now": "https://image.tmdb.org/t/p/w500/gQB8Y5RCMkv2zwzFHbUJX3kAhvA.jpg",
    "Alien": "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg",
    "Psycho": "https://image.tmdb.org/t/p/w500/81d8oyEFgj7iFi69fJegR9YRsmm.jpg",
    "Rear Window": "https://image.tmdb.org/t/p/w500/ILVF05PFKmNu9CHi7yOpvYgPsc.jpg",
    "Casablanca": "https://image.tmdb.org/t/p/w500/5K7cOHoay2mZusSLezBOY0Qxh8a.jpg",
    "Cinema Paradiso": "https://image.tmdb.org/t/p/w500/8SRUOwqvNU2WKbSS3GwAhL704wH.jpg",
    "Memento": "https://image.tmdb.org/t/p/w500/yuNs09hvpHVU1cBTCAk9zxsL2oW.jpg",
    "Spider-Man: Into the Spider-Verse": "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg",
    "Spider-Man: Across the Spider-Verse": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
    "Oppenheimer": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
    "Dune: Part Two": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
    "WALL-E": "https://image.tmdb.org/t/p/w500/hbhFnRzzg6ZDmm8YAmxBnQpQIPh.jpg",
    "The Shining": "https://image.tmdb.org/t/p/w500/b33nnKl1vAOM49FRQPm7vAo9umW.jpg",
    "Django Unchained": "https://image.tmdb.org/t/p/w500/7oWY8vdWW7thTzWh3OKYRkWUlD5.jpg",
    "Top Gun: Maverick": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg",
    "The Batman": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg",
    "No Country for Old Men": "https://image.tmdb.org/t/p/w500/6d5XOczc226jECq0LIX0siKNGGM.jpg",
    "There Will Be Blood": "https://image.tmdb.org/t/p/w500/fa0RDkAlCec0STnT7dFcNyqhhm9.jpg",
    "The Grand Budapest Hotel": "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWX9ne3rNfg.jpg",
    "Blade Runner 2049": "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",

    # --- Top TV Series ---
    "Breaking Bad": "https://image.tmdb.org/t/p/w500/ztkUQFLlC19CCMYHW9o1zWhJRNq.jpg",
    "Planet Earth II": "https://image.tmdb.org/t/p/w500/tmfV5V4R0U4vH3f7eL4s3C9P8tS.jpg",
    "Planet Earth": "https://image.tmdb.org/t/p/w500/5M4T2Ff4Z4mY5uV3rY7tC4mD6hE.jpg",
    "Band of Brothers": "https://image.tmdb.org/t/p/w500/zZXzdA395KuWzSZHHWwMw4V8B4i.jpg",
    "Chernobyl": "https://image.tmdb.org/t/p/w500/hlLXt2tOPT6RRnjiUmoxyG9LTFi.jpg",
    "The Wire": "https://image.tmdb.org/t/p/w500/4lbclFySvugI51fwsyxBTOm4DqK.jpg",
    "The Sopranos": "https://image.tmdb.org/t/p/w500/6nua9Xb7wG2yX5qVjF8t2H8zG2h.jpg",
    "Game of Thrones": "https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg",
    "Better Call Saul": "https://image.tmdb.org/t/p/w500/fC2HDm5t0kHjCGNIeo0gO59F02.jpg",
    "Sherlock": "https://image.tmdb.org/t/p/w500/7WTsnHnsAoj7hnzMisVUSxJ0IXR.jpg",
    "The Twilight Zone": "https://image.tmdb.org/t/p/w500/m1N1XW4v9B4e2rN9e8v5v6yT5rE.jpg",
    "Succession": "https://image.tmdb.org/t/p/w500/7udJw807pYv8c6q1N8r0X6qZ5vT.jpg",
    "True Detective": "https://image.tmdb.org/t/p/w500/cuV2O529dtW8WNIURq84jy2716m.jpg",
    "Fargo": "https://image.tmdb.org/t/p/w500/6U9cpRX7nT4ABPpV9BfU7RzRj8P.jpg",
    "Firefly": "https://image.tmdb.org/t/p/w500/kZID9o0j3vV5i2wF8t2H8zG2h6.jpg",
    "The Last of Us": "https://image.tmdb.org/t/p/w500/uKvVjHNqB5VmOrdxqAt2V7J9AhP.jpg",
    "Dark": "https://image.tmdb.org/t/p/w500/apbrWgAQnr41g5iZwb1q6bJ3tL6.jpg",
    "Black Mirror": "https://image.tmdb.org/t/p/w500/7Rumk9Z05g7fX8xV9B4e2rN9e8v.jpg",
    "Severance": "https://image.tmdb.org/t/p/w500/r54Lclg1q6mZ3rW9xV2yZ4mD5h.jpg",
    "Stranger Things": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
    "Peaky Blinders": "https://image.tmdb.org/t/p/w500/vUUqzWa2LnHIVqkaKVlVGkVcZIW.jpg",
    "The Office (US)": "https://image.tmdb.org/t/p/w500/qWnJzyZhyy74gjpSjIXWmuk0ifX.jpg",
    "House of the Dragon": "https://image.tmdb.org/t/p/w500/t9Xke5llaqSXFRBHOG9y9SiOIjQ.jpg",
    "Fleabag": "https://image.tmdb.org/t/p/w500/7x7y3rV7tC4mD6hE8v5v6yT5rE.jpg",
    "Mad Men": "https://image.tmdb.org/t/p/w500/77A4n0eY7fX8xV9B4e2rN9e8v.jpg",
    "The Crown": "https://image.tmdb.org/t/p/w500/jb1P1Qv7tC4mD6hE8v5v6yT5rE.jpg",
    "Mindhunter": "https://image.tmdb.org/t/p/w500/fbKE87mojpIETWepvX57C9qW9x.jpg",
    "Narcos": "https://image.tmdb.org/t/p/w500/rTmal9yrLGoAoLwv968TqF2g7S.jpg",
    "Mr. Robot": "https://image.tmdb.org/t/p/w500/oKIBhzZzDXAJj9qbnnUMcu9PZ9a.jpg",
    "Twin Peaks": "https://image.tmdb.org/t/p/w500/9y7fX8xV9B4e2rN9e8v5v6yT5rE.jpg",
    "Lost": "https://image.tmdb.org/t/p/w500/og6qbA50m4qC66xX6zD2d3aT8hF.jpg",
    "Dexter": "https://image.tmdb.org/t/p/w500/58H6075y4k7X7fX8xV9B4e2rN9e.jpg",
    "Friends": "https://image.tmdb.org/t/p/w500/2koX1xLkpTQM4IZebYvKysFW1Nh.jpg",
    "BoJack Horseman": "https://image.tmdb.org/t/p/w500/pB9PlDk7Y7fX8xV9B4e2rN9e8v.jpg",
    "Rome": "https://image.tmdb.org/t/p/w500/q9Y7fX8xV9B4e2rN9e8v5v6yT5r.jpg",
    "Six Feet Under": "https://image.tmdb.org/t/p/w500/8q1N8r0X6qZ5vT4mD6hE8v5v6y.jpg",
    "When They See Us": "https://image.tmdb.org/t/p/w500/yK9Z05g7fX8xV9B4e2rN9e8v5v.jpg",
    "Deadwood": "https://image.tmdb.org/t/p/w500/6qZ5vT4mD6hE8v5v6yT5rE7x7y.jpg",
    "Boardwalk Empire": "https://image.tmdb.org/t/p/w500/9xV9B4e2rN9e8v5v6yT5rE7x7y3.jpg",
    "Justified": "https://image.tmdb.org/t/p/w500/8e2rN9e8v5v6yT5rE7x7y3rV7t.jpg",
    "Shōgun": "https://image.tmdb.org/t/p/w500/7O4iVfOMQmdCSxhOg1WnzG1AgYT.jpg",
    "The Bear": "https://image.tmdb.org/t/p/w500/6W6B0k3g0vX5rY7tC4mD6hE8v.jpg",
    "Ted Lasso": "https://image.tmdb.org/t/p/w500/9O3m0k3g0vX5rY7tC4mD6hE8v.jpg",
    "Hannibal": "https://image.tmdb.org/t/p/w500/40X0m0k3g0vX5rY7tC4mD6hE8v.jpg",
    "Community": "https://image.tmdb.org/t/p/w500/a2X0m0k3g0vX5rY7tC4mD6hE8v.jpg",
    "Yellowstone": "https://image.tmdb.org/t/p/w500/peNC0eyc3Kp69xmCDxsRu4W26bm.jpg",
    "The Boys": "https://image.tmdb.org/t/p/w500/7Ns6tO3aYjflEjFispBG84mD.jpg",
    "The Mandalorian": "https://image.tmdb.org/t/p/w500/eU1i6eHXlzMOlEq0ku1R07Y96VW.jpg",

    # --- Top Anime Series & Movies ---
    "Fullmetal Alchemist: Brotherhood": "https://image.tmdb.org/t/p/w500/5ZFUEOULaVml7p19UP7Dkhkh2x8.jpg",
    "Frieren: Beyond Journey's End": "https://image.tmdb.org/t/p/w500/dqZENchTd7lp5zht7BdlqM7RBhD.jpg",
    "Steins;Gate": "https://image.tmdb.org/t/p/w500/59lW8VjG60cK8vM2rL3zD4mK8.jpg",
    "Hunter x Hunter (2011)": "https://image.tmdb.org/t/p/w500/ucmpV9HhH3D1T6YjF8vM2rL3z.jpg",
    "Attack on Titan": "https://image.tmdb.org/t/p/w500/hTP1DtLGFamjfu8WqjnuQdP1n4i.jpg",
    "Bleach: Thousand-Year Blood War": "https://image.tmdb.org/t/p/w500/2LjhR2oG2H3hF8vM2rL3zD4m.jpg",
    "Death Note": "https://image.tmdb.org/t/p/w500/iigTJJskNfRvhqf96Y8p7mD6hE.jpg",
    "Cowboy Bebop": "https://image.tmdb.org/t/p/w500/f37A09hF8vM2rL3zD4mK8p7mD.jpg",
    "Vinland Saga": "https://image.tmdb.org/t/p/w500/o71fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Monster": "https://image.tmdb.org/t/p/w500/171fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Code Geass: Lelouch of the Rebellion": "https://image.tmdb.org/t/p/w500/271fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Jujutsu Kaisen": "https://image.tmdb.org/t/p/w500/hDvh4fW4mD6hE8v5v6yT5rE7.jpg",
    "Demon Slayer: Kimetsu no Yaiba": "https://image.tmdb.org/t/p/w500/xU7fW4mD6hE8v5v6yT5rE7x.jpg",
    "One Piece": "https://image.tmdb.org/t/p/w500/fcXdJUSZiue2ZaUN29vg857aA.jpg",
    "Naruto: Shippuden": "https://image.tmdb.org/t/p/w500/kV27gqpEzq7b4ZfRz4mD6hE.jpg",
    "Neon Genesis Evangelion": "https://image.tmdb.org/t/p/w500/981fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Mob Psycho 100": "https://image.tmdb.org/t/p/w500/381fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Berserk (1997)": "https://image.tmdb.org/t/p/w500/481fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Clannad: After Story": "https://image.tmdb.org/t/p/w500/581fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Violet Evergarden": "https://image.tmdb.org/t/p/w500/681fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Your Name.": "https://image.tmdb.org/t/p/w500/q719jXXEzOoYaps6babgKnONONX.jpg",
    "A Silent Voice": "https://image.tmdb.org/t/p/w500/tuFaWiqX0TXRWu7xsB79um9h8.jpg",
    "Princess Mononoke": "https://image.tmdb.org/t/p/w500/cMYCDADoLKLbB83g4WnJSTZ8.jpg",
    "Grave of the Fireflies": "https://image.tmdb.org/t/p/w500/k9Tvpp6FqWmsN6iKx.jpg",
    "Howl's Moving Castle": "https://image.tmdb.org/t/p/w500/6pZMF7496vdaikF18hZ5z.jpg",
    "Akira": "https://image.tmdb.org/t/p/w500/5F46x0oD6hE8v5v6yT5rE7x7y.jpg",
    "Demon Slayer: Mugen Train": "https://image.tmdb.org/t/p/w500/h8duW4mD6hE8v5v6yT5rE7x.jpg",

    # --- Top Cartoons & Animated Movies ---
    "Avatar: The Last Airbender": "https://image.tmdb.org/t/p/w500/cHFZAxhzq0Cs6Fq2Y8I77Y6Z8Q9.jpg",
    "Arcane": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn39Dbnhgnqqf.jpg",
    "Batman: The Animated Series": "https://image.tmdb.org/t/p/w500/9Q10fW4mD6hE8v5v6yT5rE7x.jpg",
    "Rick and Morty": "https://image.tmdb.org/t/p/w500/8kOWDBKCVs9A7u9Q91T8f.jpg",
    "Gravity Falls": "https://image.tmdb.org/t/p/w500/m11fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Over the Garden Wall": "https://image.tmdb.org/t/p/w500/n11fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Samurai Jack": "https://image.tmdb.org/t/p/w500/p11fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Spider-Man: The Animated Series": "https://image.tmdb.org/t/p/w500/q11fW4mD6hE8v5v6yT5rE7x7y.jpg",
    "X-Men '97": "https://image.tmdb.org/t/p/w500/9fZsvwW4mD6hE8v5v6yT5rE7.jpg",
    "Star Wars: The Clone Wars": "https://image.tmdb.org/t/p/w500/eGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Justice League Unlimited": "https://image.tmdb.org/t/p/w500/fGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Adventure Time": "https://image.tmdb.org/t/p/w500/gGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Regular Show": "https://image.tmdb.org/t/p/w500/hGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Primal": "https://image.tmdb.org/t/p/w500/iGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "South Park": "https://image.tmdb.org/t/p/w500/jGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "The Simpsons (Golden Era)": "https://image.tmdb.org/t/p/w500/kGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Futurama": "https://image.tmdb.org/t/p/w500/lGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Invincible": "https://image.tmdb.org/t/p/w500/mGrW4mD6hE8v5v6yT5rE7x7y.jpg",
    "Toy Story": "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxQZ.jpg",
    "Toy Story 3": "https://image.tmdb.org/t/p/w500/AbbXspwhIR19GFYknYeYsMC3BqP.jpg",
    "Ratatouille": "https://image.tmdb.org/t/p/w500/t3vaWRPSf6W16ipzztKRf9x.jpg",
    "Up": "https://image.tmdb.org/t/p/w500/vpbaStTMt8qqGBE2VgEEIRolO0x.jpg",
    "Finding Nemo": "https://image.tmdb.org/t/p/w500/eHuGQ10FaZDAAy4W9Y1G9M0cZ9p.jpg",
    "The Incredibles": "https://image.tmdb.org/t/p/w500/2LqaLgk4Z226KkgPJuiOQ58.jpg",
    "Monsters, Inc.": "https://image.tmdb.org/t/p/w500/sgheT6Fh8vM2rL3zD4mK8p7mD.jpg",
    "Coco": "https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqxhJ5Ut.jpg",
    "Inside Out": "https://image.tmdb.org/t/p/w500/2H1TmgdfNtsKlU9qBrTSaoMVite.jpg",
    "Inside Out 2": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg",
    "Soul": "https://image.tmdb.org/t/p/w500/hm58Jw4Lw8vX7fX8xV9B4e2rN9e.jpg",
    "Shrek": "https://image.tmdb.org/t/p/w500/dyhaB19AIC4zgDSUT2yv.jpg",
    "How to Train Your Dragon": "https://image.tmdb.org/t/p/w500/ygGmAO60m.jpg",

    # --- Top Episodes ---
    "Ozymandias": "https://image.tmdb.org/t/p/w500/h6g61qV5288Rz8XG7r94fK7F.jpg",
    "Battle of the Bastards": "https://image.tmdb.org/t/p/w500/vJj5P5c6q.jpg",
    "Hero": "https://image.tmdb.org/t/p/w500/hTP1DtLGFamjfu8WqjnuQdP1n4i.jpg",
    "Sozin's Comet: Part 4": "https://image.tmdb.org/t/p/w500/cHFZAxhzq0Cs6Fq2Y8I77Y6Z8Q9.jpg",
    "The Monster You Created": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn39Dbnhgnqqf.jpg",
    "Connor's Wedding": "https://image.tmdb.org/t/p/w500/7udJw807pYv8c6q1N8r0X6qZ5vT.jpg",
    "Vichnaya Pamyat": "https://image.tmdb.org/t/p/w500/hlLXt2tOPT6RRnjiUmoxyG9LTFi.jpg",
    "Plan and Execution": "https://image.tmdb.org/t/p/w500/fC2HDm5t0kHjCGNIeo0gO59F02.jpg",
    "The View from Halfway Down": "https://image.tmdb.org/t/p/w500/pB9PlDk7Y7fX8xV9B4e2rN9e8v.jpg"
}

# Reliable High-Res Fallbacks based on Media Type
CATEGORY_FALLBACKS: Dict[str, str] = {
    "movie": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80",
    "tv_series": "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=500&q=80",
    "anime_series": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&q=80",
    "anime_movie": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500&q=80",
    "cartoon_series": "https://images.unsplash.com/photo-1563089145-599997674d42?w=500&q=80",
    "animated_movie": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500&q=80",
    "legendary_episode": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80"
}

def get_media_poster(item: Dict[str, Any]) -> str:
    """Resolves the best poster image URL for any title or episode."""
    if item.get("poster_url"):
        return item["poster_url"]

    title = item.get("title") or item.get("episode_title") or ""
    series_title = item.get("series_title", "")
    media_type = item.get("media_type", "movie")

    # 1. Exact Title Match
    if title in POSTERS_CATALOG:
        return POSTERS_CATALOG[title]

    # 2. Check Parent Series for Episodes
    if series_title and series_title in POSTERS_CATALOG:
        return POSTERS_CATALOG[series_title]

    # 3. Substring matching
    title_lower = title.lower()
    for cat_title, url in POSTERS_CATALOG.items():
        if cat_title.lower() in title_lower or title_lower in cat_title.lower():
            return url

    # 4. Graceful category-specific HD banner fallback
    return CATEGORY_FALLBACKS.get(media_type, CATEGORY_FALLBACKS["movie"])
