from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from backend.app.config.llm_factory import LLMFactory
from backend.app.observability.logger import logger
from backend.app.schemas.itinerary import Itinerary, ItineraryActivity, ItineraryDay
from backend.app.schemas.travel_state import TravelState
from mcp_servers.travel_server.server import search_attractions


class ItineraryAgent:
    """Specialist Agent responsible for synthesizing day-by-day activity schedules."""

    DESTINATION_THEMES: dict[str, list[dict[str, str]]] = {
        "shimla": [
            {
                "theme": "Arrival, Mall Road Promenade & Heritage Christ Church",
                "morning": (
                    "Arrival & Hotel Check-in",
                    "Arrive in Shimla via scenic Kalka toy train/car, check into hotel.",
                    "Shimla Mall Road",
                    0.0,
                ),
                "afternoon": (
                    "The Ridge & Christ Church Heritage Walk",
                    "Walk along famous open Ridge plaza, visit Neo-Gothic 1857 Christ Church.",
                    "The Ridge, Shimla",
                    500.0,
                ),
                "evening": (
                    "Lakkar Bazaar Shopping & Himachali Dinner",
                    "Browse wooden handicrafts, enjoy steaming Momos and Siddu at local eatery.",
                    "Lakkar Bazaar",
                    1200.0,
                ),
            },
            {
                "theme": "Kufri Snow Point, Adventure Activities & Pine Forest Walk",
                "morning": (
                    "Kufri Snow Point Excursion",
                    "Excursion to Kufri for snow views, horse riding, and Himalayan Nature Park.",
                    "Kufri Snow Park",
                    2500.0,
                ),
                "afternoon": (
                    "Tobogganing & Skiing in Kufri",
                    "Experience thrilling toboggan rides and snow sports amidst pine valley.",
                    "Kufri Fun World",
                    2000.0,
                ),
                "evening": (
                    "Café Hopping on Mall Road",
                    "Warm up with hot chocolate and Pahadi teas at colonial cafes.",
                    "Mall Road",
                    1500.0,
                ),
            },
            {
                "theme": "Jakhoo Temple Cable Car & Viceregal Lodge",
                "morning": (
                    "Jakhoo Temple Ropeway & Hanuman Statue",
                    "Cable car ride to Jakhoo Hill (8054 ft) and visit 108ft Lord Hanuman statue.",
                    "Jakhoo Hill",
                    1000.0,
                ),
                "afternoon": (
                    "Viceregal Lodge & Indian Institute of Advanced Study",
                    "Tour magnificent Jacobethan architecture estate and botanical gardens.",
                    "Observatory Hill",
                    800.0,
                ),
                "evening": (
                    "Sunset Point & Departure Transfer",
                    "Capture panoramic Himalayan valley sunset views before return journey.",
                    "Scandal Point",
                    500.0,
                ),
            },
        ],
        "kashmir": [
            {
                "theme": "Srinagar Arrival, Dal Lake Shikara Ride & Houseboat Check-in",
                "morning": (
                    "Srinagar Airport Arrival & Transfer",
                    "Arrive at Sheikh ul-Alam International Airport, transfer to Dal Lake.",
                    "Srinagar",
                    0.0,
                ),
                "afternoon": (
                    "Luxury Houseboat Check-in & Kashmiri Wazwan Lunch",
                    "Check into handcrafted wooden houseboat, savor authentic Kashmiri Wazwan meal.",
                    "Dal Lake Houseboat",
                    2500.0,
                ),
                "evening": (
                    "Sunset Shikara Ride & Floating Market",
                    "Glide past lotus gardens and floating flower markets in wooden Shikara boat.",
                    "Dal Lake",
                    1500.0,
                ),
            },
            {
                "theme": "Gulmarg Snow Gondola Cable Car & Skiing Adventure",
                "morning": (
                    "Drive to Gulmarg & Phase 1 Gondola Ride",
                    "Scenic drive to Gulmarg ('Meadow of Flowers') and take Phase 1 Gondola cable car to Kongdoori.",
                    "Gulmarg Gondola Station",
                    3500.0,
                ),
                "afternoon": (
                    "Phase 2 Apharwat Peak Snow Point & Skiing",
                    "Ascend to 13,780 ft snow slopes of Apharwat Peak for snow play and skiing.",
                    "Apharwat Peak",
                    3000.0,
                ),
                "evening": (
                    "Warm Kahwa Tea at Pine Resort",
                    "Sip hot Kashmiri Kahwa tea infused with saffron, cardamom and almonds.",
                    "Gulmarg Resort",
                    800.0,
                ),
            },
            {
                "theme": "Pahalgam Valley of Shepherds & Betaab Valley",
                "morning": (
                    "Drive to Pahalgam via Saffron Fields & Awantipora",
                    "Visit Pampore saffron fields and ancient Awantipora temple ruins.",
                    "Pahalgam Highway",
                    1200.0,
                ),
                "afternoon": (
                    "Betaab Valley & Aru Valley Excursion",
                    "Explore pristine pine forest valleys, snow-fed stream streams, and pony rides.",
                    "Betaab Valley",
                    2000.0,
                ),
                "evening": (
                    "Lidder River Riverside Dining",
                    "Enjoy grilled trout fish dinner along gushing Lidder river banks.",
                    "Lidder Riverfront",
                    2200.0,
                ),
            },
            {
                "theme": "Mughal Gardens & Pashmina Handicraft Shopping",
                "morning": (
                    "Shalimar Bagh & Nishat Bagh Mughal Gardens",
                    "Walk through terraced lawns, cascading fountains, and historic Chinar trees.",
                    "Boulevard Road",
                    1000.0,
                ),
                "afternoon": (
                    "Pashmina Shawl & Saffron Shopping",
                    "Shop for authentic hand-woven Kashmiri Pashmina shawls, dry fruits, and saffron.",
                    "Lal Chowk Srinagar",
                    3000.0,
                ),
                "evening": (
                    "Departure Transfer",
                    "Transfer to Srinagar Airport for onward flight home with magical snow memories.",
                    "Srinagar Airport",
                    0.0,
                ),
            },
        ],
        "goa": [
            {
                "theme": "Arrival, Hotel Check-in & Calangute Beach Sunset",
                "morning": (
                    "Arrival & Airport Transfer",
                    "Land at Goa Dabolim/MOPA Airport, collect baggage and proceed to resort.",
                    "Airport",
                    0.0,
                ),
                "afternoon": (
                    "Resort Check-in & Goan Fish Curry Lunch",
                    "Settle into room and savor authentic Goan prawn/fish curry.",
                    "Beach Resort",
                    1200.0,
                ),
                "evening": (
                    "Calangute & Baga Beach Sunset Walk",
                    "Stroll along famous golden sand beaches and enjoy beach shack music.",
                    "Calangute Beach",
                    500.0,
                ),
            },
            {
                "theme": "Fontainhas Latin Quarter & Historic Old Goa Churches",
                "morning": (
                    "Fontainhas Portuguese Heritage Walk",
                    "Explore colorful Latin quarter streets, heritage homes, and art galleries.",
                    "Panjim",
                    1500.0,
                ),
                "afternoon": (
                    "Old Goa UNESCO Basilica Tour",
                    "Visit Basilica of Bom Jesus and Se Cathedral built in 16th century.",
                    "Old Goa",
                    800.0,
                ),
                "evening": (
                    "Mandovi River Cruise & Dinner",
                    "Enjoy traditional Goan folk dance and dinner on Mandovi river cruise boat.",
                    "Panjim Jetty",
                    2200.0,
                ),
            },
            {
                "theme": "Dudhsagar Waterfalls & Spice Plantation Excursion",
                "morning": (
                    "Jeep Safari to Dudhsagar Waterfalls",
                    "Exhilarating 4x4 jeep trek through Bhagwan Mahavir Wildlife Sanctuary.",
                    "Dudhsagar",
                    3000.0,
                ),
                "afternoon": (
                    "Organic Spice Plantation Lunch",
                    "Traditional buffet lunch served on banana leaf with guided spice tour.",
                    "Ponda",
                    1000.0,
                ),
                "evening": (
                    "Spice Tasting & Herbal Shopping",
                    "Sample organic spices, cashew feni, and return to hotel for relaxed evening.",
                    "Ponda",
                    500.0,
                ),
            },
            {
                "theme": "Water Sports & Anjuna Night Market Experience",
                "morning": (
                    "Anjuna & Vagator Watersports",
                    "Parasailing, jet-skiing, and banana boat rides at Anjuna beach.",
                    "Anjuna Beach",
                    3500.0,
                ),
                "afternoon": (
                    "Fort Aguada & Lighthouse Viewpoint",
                    "Panoramic views of Arabian Sea from 17th-century Portuguese fortress.",
                    "Sinquerim",
                    400.0,
                ),
                "evening": (
                    "Curlies Shack Dinner & Live Music",
                    "Vibrant seaside dining with fresh grilled seafood and live acoustic music.",
                    "Anjuna Shack",
                    2500.0,
                ),
            },
            {
                "theme": "Souvenir Shopping & Airport Departure",
                "morning": (
                    "Panjim Market Cashew & Craft Shopping",
                    "Buy local Goan cashews, spices, handicrafts, and feni.",
                    "Panjim Market",
                    1500.0,
                ),
                "afternoon": (
                    "Check-out & Flight Transfer",
                    "Hotel check-out and private transfer to airport for return flight.",
                    "Goa Airport",
                    1200.0,
                ),
                "evening": (
                    "Departure Flight",
                    "Board return flight home with wonderful coastal memories.",
                    "Airport",
                    0.0,
                ),
            },
        ],
        "dubai": [
            {
                "theme": "Arrival, Hotel Check-in & Dubai Marina Walk",
                "morning": (
                    "Arrival & Airport Transfer",
                    "Land at Dubai International Airport (DXB) and private transfer.",
                    "DXB Airport",
                    0.0,
                ),
                "afternoon": (
                    "Hotel Check-in & Lunch",
                    "Settle into hotel room and enjoy Mediterranean lunch.",
                    "Hotel Restaurant",
                    2000.0,
                ),
                "evening": (
                    "Dubai Marina Promenade Sunset Stroll",
                    "Walk along luxury yacht marina surrounded by illuminated skyscrapers.",
                    "Dubai Marina",
                    1000.0,
                ),
            },
            {
                "theme": "Burj Khalifa, Dubai Mall & Fountain Show",
                "morning": (
                    "Burj Khalifa 124th Floor Observation Deck",
                    "Panoramic 360-degree views from world's tallest building.",
                    "Downtown Dubai",
                    4500.0,
                ),
                "afternoon": (
                    "Dubai Mall Shopping & Aquarium",
                    "Explore world's largest mall and visit Dubai Aquarium & Underwater Zoo.",
                    "Dubai Mall",
                    3000.0,
                ),
                "evening": (
                    "Dubai Fountain Light & Musical Show",
                    "Spectacular dancing water fountain show set to global music tracks.",
                    "Burj Park",
                    1500.0,
                ),
            },
            {
                "theme": "Desert Safari & Sunset Dunes BBQ Night",
                "morning": (
                    "Leisurely Breakfast & Gold Souk Walk",
                    "Explore traditional Deira Gold & Spice Souk markets.",
                    "Deira",
                    1000.0,
                ),
                "afternoon": (
                    "4x4 Dune Bashing & Camel Ride",
                    "Thrilling desert sand dune bashing, sandboarding, and camel riding.",
                    "Lahbab Desert",
                    4000.0,
                ),
                "evening": (
                    "Arabian Desert Camp BBQ & Belly Dance",
                    "Al fresco Arabian buffet dinner with tanoura dance and henna painting.",
                    "Desert Camp",
                    2500.0,
                ),
            },
            {
                "theme": "Palm Jumeirah & Atlantis Aquaventure",
                "morning": (
                    "Palm Jumeirah Monorail & Atlantis Tour",
                    "Scenic monorail ride across man-made Palm island to Atlantis resort.",
                    "Palm Jumeirah",
                    2000.0,
                ),
                "afternoon": (
                    "Aquaventure Waterpark Thrills",
                    "World-class water slides and lazy river tubing at Atlantis.",
                    "Atlantis The Palm",
                    5500.0,
                ),
                "evening": (
                    "Seafood Dinner at The Pointe",
                    "Seafood dining with front-row view of Palm Fountains.",
                    "The Pointe",
                    3000.0,
                ),
            },
            {
                "theme": "Museum of the Future & Departure",
                "morning": (
                    "Museum of the Future Interactive Tour",
                    "Futuristic architectural masterpiece showcasing innovative technology.",
                    "Sheikh Zayed Rd",
                    3500.0,
                ),
                "afternoon": (
                    "Check-out & DXB Airport Transfer",
                    "Hotel check-out and transfer to airport for onward flight.",
                    "DXB Airport",
                    1500.0,
                ),
                "evening": (
                    "Return Flight Departure",
                    "Board return flight home.",
                    "DXB Airport",
                    0.0,
                ),
            },
        ],
    }

    @classmethod
    def get_template(cls, destination: str, day_idx: int) -> dict[str, Any]:
        dest_key = destination.lower().strip()
        templates = cls.DESTINATION_THEMES.get(dest_key)
        if templates:
            return templates[(day_idx - 1) % len(templates)]

        # Try dynamic MCP Attraction lookup
        try:
            attraction_data = search_attractions(destination)
            if attraction_data and len(attraction_data) >= 3:
                a1 = attraction_data[(day_idx * 3 - 3) % len(attraction_data)]
                a2 = attraction_data[(day_idx * 3 - 2) % len(attraction_data)]
                a3 = attraction_data[(day_idx * 3 - 1) % len(attraction_data)]
                return {
                    "theme": f"Day {day_idx} Exploration of {destination} ({a1['name']} & Cultural Highlights)",
                    "morning": (
                        a1["name"],
                        a1["description"],
                        f"District 1, {destination}",
                        float(a1.get("estimated_cost_inr", 1500.0)),
                    ),
                    "afternoon": (
                        a2["name"],
                        a2["description"],
                        f"Cultural Center, {destination}",
                        float(a2.get("estimated_cost_inr", 1800.0)),
                    ),
                    "evening": (
                        a3["name"],
                        a3["description"],
                        f"Promenade, {destination}",
                        float(a3.get("estimated_cost_inr", 2200.0)),
                    ),
                }
        except Exception:
            pass

        # Distinct daily themes if offline
        day_themes = [
            {
                "theme": f"Day {day_idx} City Arrival & Landmark Heritage Walk",
                "morning": ("City Orientation & Hotel Check-in", f"Arrive in {destination}, transfer to hotel and settle in.", f"Central {destination}", 0.0),
                "afternoon": ("Historic District & Main Plaza Tour", f"Guided walking tour of {destination} landmark square and historic architecture.", f"Old Town {destination}", 1500.0),
                "evening": ("Welcome Dinner & Local Culinary Tasting", f"Savor authentic regional cuisine at a top-rated traditional bistro.", f"{destination} Market Square", 2500.0),
            },
            {
                "theme": f"Day {day_idx} Arts, Museums & Cultural Exploration",
                "morning": ("National Museum & Art Gallery Visit", f"Explore key art collections and historical exhibits of {destination}.", f"Cultural District {destination}", 1200.0),
                "afternoon": ("Local Artisan Bazaar & Souk Shopping", f"Browse local handicrafts, spices, and artisan souvenirs in {destination}.", f"Bazaar District {destination}", 1800.0),
                "evening": ("Panoramic Sunset Viewpoint & Fine Dining", f"Watch sunset views over {destination} skyline followed by dinner.", f"{destination} Promenade", 2800.0),
            },
            {
                "theme": f"Day {day_idx} Nature, Parks & Riverfront Promenade",
                "morning": ("Botanical Gardens & Waterfront Walk", f"Morning stroll through scenic public gardens and riverfront paths in {destination}.", f"Waterfront {destination}", 500.0),
                "afternoon": ("Iconic Monument & Architectural Highlights", f"Visit famous architectural wonders and photogenic spots.", f"Central Boulevard {destination}", 2000.0),
                "evening": ("Night Market & Acoustic Live Music", f"Vibrant evening exploring street food stalls and live local acoustic music.", f"Night Market {destination}", 2200.0),
            },
        ]
        return day_themes[(day_idx - 1) % len(day_themes)]

    @classmethod
    def generate(
        cls,
        destination: str = "Goa",
        destinations: list[str] | None = None,
        duration_days: int = 5,
        preferences: list[str] | None = None,
    ) -> Itinerary:
        """Generate detailed day-by-day itinerary supporting single or multi-destination trips."""
        target_dests = destinations if destinations and len(destinations) > 0 else [destination]

        # Try Groq LLM structured generation when API key is configured
        if LLMFactory.is_groq_available():
            try:
                llm = LLMFactory.get_chat_model(temperature=0.3)
                structured_llm = llm.with_structured_output(Itinerary)
                prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "You are an expert travel itinerary specialist. Generate a comprehensive, realistic day-by-day travel itinerary for the target destination(s). Make sure EVERY day has a unique, non-repeating theme, location, and 3 activities (Morning, Afternoon, Evening) with realistic costs in INR.",
                        ),
                        (
                            "human",
                            "Create a {duration_days}-day travel itinerary for {dest_str}. Preferences: {pref_str}",
                        ),
                    ]
                )
                chain = prompt | structured_llm
                dest_str = " & ".join(target_dests)
                pref_str = ", ".join(preferences) if preferences else "general sightseeing and culture"
                res: Itinerary = chain.invoke(
                    {
                        "duration_days": duration_days,
                        "dest_str": dest_str,
                        "pref_str": pref_str,
                    }
                )
                if res and res.days and len(res.days) > 0:
                    return res
            except Exception as e:
                logger.warning("Groq LLM itinerary generation failed, falling back to dynamic provider", error=str(e))

        # Dynamic fallback generation
        days: list[ItineraryDay] = []
        num_dests = len(target_dests)

        # Allocate days per destination
        days_per_dest = duration_days // num_dests
        extra_days = duration_days % num_dests

        current_dest_idx = 0
        days_in_current_dest = 0
        target_days_for_current = days_per_dest + (1 if current_dest_idx < extra_days else 0)

        for i in range(1, duration_days + 1):
            city = target_dests[current_dest_idx]
            day_in_city = days_in_current_dest + 1
            tmpl = cls.get_template(city, day_in_city)
            activities: list[ItineraryActivity] = []

            # Check if this day is a transit day between cities
            is_transit_day = num_dests > 1 and day_in_city == 1 and current_dest_idx > 0

            if is_transit_day:
                prev_city = target_dests[current_dest_idx - 1]
                m_title, m_desc, m_loc, m_cost = (
                    f"Inter-city Transit: {prev_city} → {city}",
                    f"Check out from {prev_city} hotel, private transfer/high-speed transport to {city}.",
                    f"Transit Route ({prev_city} - {city})",
                    2500.0,
                )
            else:
                m_title, m_desc, m_loc, m_cost = tmpl["morning"]

            a_title, a_desc, a_loc, a_cost = tmpl["afternoon"]
            e_title, e_desc, e_loc, e_cost = tmpl["evening"]

            activities.append(
                ItineraryActivity(
                    time_slot="09:00 AM - 12:30 PM",
                    activity_title=m_title,
                    description=m_desc,
                    location=m_loc,
                    cost_inr=float(m_cost),
                )
            )
            activities.append(
                ItineraryActivity(
                    time_slot="01:30 PM - 05:00 PM",
                    activity_title=a_title,
                    description=a_desc,
                    location=a_loc,
                    cost_inr=float(a_cost),
                )
            )
            activities.append(
                ItineraryActivity(
                    time_slot="06:30 PM - 09:30 PM",
                    activity_title=e_title,
                    description=e_desc,
                    location=e_loc,
                    cost_inr=float(e_cost),
                )
            )

            daily_cost = sum(act.cost_inr for act in activities)
            days.append(
                ItineraryDay(
                    day_number=i,
                    date=f"Day {i}",
                    destination_city=city,
                    theme=f"[{city}] {tmpl['theme']}",
                    activities=activities,
                    daily_cost_inr=daily_cost,
                )
            )

            days_in_current_dest += 1
            if days_in_current_dest >= target_days_for_current and current_dest_idx < num_dests - 1:
                current_dest_idx += 1
                days_in_current_dest = 0
                target_days_for_current = days_per_dest + (
                    1 if current_dest_idx < extra_days else 0
                )

        dest_str = " & ".join(target_dests) if num_dests > 1 else target_dests[0]
        summary = f"Comprehensive {duration_days}-day multi-city itinerary for {dest_str} balancing sightseeing, inter-city travel, and local culture."
        highlights = [
            f"Seamless travel itinerary covering {dest_str}",
            "Balanced allocation of days and curated local cultural tours in each city",
            "Included inter-city transit and smooth hotel check-ins",
            "Zero scheduling overlaps between flights, hotel check-ins, and tours",
        ]

        return Itinerary(
            destination=dest_str,
            destinations=target_dests,
            total_days=duration_days,
            days=days,
            summary=summary,
            highlights=highlights,
        )

    @classmethod
    def run_node(cls, state: TravelState) -> TravelState:
        """Execute Itinerary Agent as a LangGraph node handler."""
        decision = state.get("supervisor_decision")
        destinations = state.get("destinations") or (
            decision.destinations if decision and decision.destinations else []
        )
        destination = state.get("destination") or (decision.destination if decision else "Goa")
        if not destinations:
            destinations = [destination]

        duration = decision.duration_days if decision else 5
        travelers = decision.travelers if decision else 2
        origin = state.get("origin") or "Bangalore"
        preferences = state.get("preferences") or []

        itinerary = cls.generate(
            destination=destination,
            destinations=destinations,
            duration_days=duration,
            preferences=preferences,
        )

        flight_res = state.get("flight_results")
        hotel_res = state.get("hotel_results")
        weather_res = state.get("weather_results")
        budget_res = state.get("budget_analysis")

        # Synthesize complete, detailed markdown document
        lines: list[str] = [
            f"# ✈️ Complete Travel Plan & Itinerary: {itinerary.destination}",
            f"**Origin**: {origin} | **Destinations**: {', '.join(destinations)} | **Travelers**: {travelers} | **Duration**: {duration} Days\n",
            "---",
            "## ✈️ Flight Options (MCP Live Search)",
        ]

        if flight_res and flight_res.options:
            lines.append(
                "| Airline | Flight No | Departure | Arrival | Duration | Price / Person | Total Flight Cost |"
            )
            lines.append("|---|---|---|---|---|---|---|")
            for f in flight_res.options:
                lines.append(
                    f"| **{f.airline}** | `{f.flight_number}` | {f.departure_time} | {f.arrival_time} | {f.duration} | ₹{f.price_inr:,.2f} | **₹{f.total_price_inr:,.2f}** |"
                )
        else:
            lines.append("_No flight data returned._")

        lines.extend(
            [
                "\n## 🏨 Lodging & Accommodation Options (MCP Live Search)",
            ]
        )

        if hotel_res and hotel_res.options:
            lines.append(
                f"| Hotel Name | Location | Rating | Price / Night | Total Stay ({hotel_res.nights} Nights) | Key Amenities |"
            )
            lines.append("|---|---|---|---|---|---|")
            for h in hotel_res.options:
                amenities_str = ", ".join(h.amenities[:3]) if h.amenities else "WiFi, AC, Breakfast"
                lines.append(
                    f"| **{h.hotel_name}** | {h.location} | ⭐ {h.rating}/5 | ₹{h.price_per_night_inr:,.2f} | **₹{h.total_price_inr:,.2f}** | {amenities_str} |"
                )
        else:
            lines.append("_No hotel data returned._")

        lines.extend(
            [
                "\n## 🌤️ Live Weather Forecast (Open-Meteo Integration)",
            ]
        )

        if weather_res:
            lines.append(f"**Current Status**: {weather_res.weather_summary}\n")
            lines.append("| Day / Date | Max Temp | Min Temp | Condition | Rain Probability |")
            lines.append("|---|---|---|---|---|")
            for w in weather_res.forecast:
                lines.append(
                    f"| {w.date} | {w.temp_max_c:.1f}°C | {w.temp_min_c:.1f}°C | {w.weather_condition} | {w.precipitation_prob}% |"
                )
            if weather_res.recommendations:
                lines.append("\n**Packing & Weather Tips**:")
                for rec in weather_res.recommendations:
                    lines.append(f"- {rec}")
        else:
            lines.append("_No weather data available._")

        lines.extend(
            [
                "\n## 💰 Financial & Budget Analysis",
            ]
        )

        if budget_res:
            lines.append(
                f"**Budget Limit**: ₹{budget_res.budget_limit:,.2f} | **Estimated Total**: ₹{budget_res.estimated_total:,.2f} | **Status**: `{budget_res.status_label}`\n"
            )
            lines.append("| Expense Category | Estimated Cost (INR) | % of Budget |")
            lines.append("|---|---|---|")
            cb = budget_res.cost_breakdown
            limit = budget_res.budget_limit or 1.0
            lines.append(f"| ✈️ Flights | ₹{cb.flights:,.2f} | {(cb.flights / limit) * 100:.1f}% |")
            lines.append(
                f"| 🏨 Accommodation | ₹{cb.accommodation:,.2f} | {(cb.accommodation / limit) * 100:.1f}% |"
            )
            lines.append(f"| 🍽️ Food & Dining | ₹{cb.food:,.2f} | {(cb.food / limit) * 100:.1f}% |")
            lines.append(
                f"| 🚕 Local Transport | ₹{cb.transport:,.2f} | {(cb.transport / limit) * 100:.1f}% |"
            )
            lines.append(
                f"| 🎟️ Tours & Activities | ₹{cb.activities:,.2f} | {(cb.activities / limit) * 100:.1f}% |"
            )
            lines.append(
                f"| 🛍️ Miscellaneous Buffer | ₹{cb.miscellaneous:,.2f} | {(cb.miscellaneous / limit) * 100:.1f}% |"
            )
            lines.append(
                f"| **TOTAL ESTIMATED** | **₹{budget_res.estimated_total:,.2f}** | **{(budget_res.estimated_total / limit) * 100:.1f}%** |"
            )
        else:
            lines.append("_No budget analysis available._")

        lines.extend(
            [
                "\n## 📅 Detailed Day-by-Day Itinerary Schedule\n",
            ]
        )

        for day in itinerary.days:
            lines.append(
                f"### 🗓️ Day {day.day_number} [{day.destination_city or destination}]: {day.theme}"
            )
            lines.append(f"*Estimated Daily Activity Expense: ₹{day.daily_cost_inr:,.2f}*\n")
            lines.append("| Time Slot | Activity | Description | Location | Est. Cost |")
            lines.append("|---|---|---|---|---|")
            for act in day.activities:
                lines.append(
                    f"| `{act.time_slot}` | **{act.activity_title}** | {act.description} | {act.location} | ₹{act.cost_inr:,.2f} |"
                )
            lines.append("")

        lines.extend(
            [
                "---",
                "### 📌 Key Highlights & Travel Notes",
            ]
        )
        for h in itinerary.highlights:
            lines.append(f"- {h}")

        lines.append(
            "\n*Demo Mode Notice: Flight and hotel options are generated via simulated MCP providers. Weather forecasts use live Open-Meteo API when available.*"
        )

        synth_response = "\n".join(lines)

        return {
            "itinerary": itinerary,
            "final_response": synth_response,
        }
