#Ron Moen 
class AgribusinessAdvisor:
    def __init__(self):
        self.crops = {
            "Rift Valley": "Maize",
            "Central Kenya": "Dairy",
            "Meru": "Miraa"
        }
        self.practices = {
            "soil_health": "Regularly test soil and add organic matter.",
            "pest_control": "Use integrated pest management techniques.",
            "irrigation": "Implement drip irrigation for water efficiency."
        }
        self.market_access = {
            "find_buyers": "Connect with local cooperatives and online platforms.",
            "pricing_trends": "Check local market reports and agricultural fairs."
        }
        self.value_addition = {
            "drying_fruits": "Invest in solar dryers for fruits.",
            "packaging_honey": "Use attractive packaging to enhance sales."
        }

    def get_crop_selection(self, region):
        return self.crops.get(region, "No data available for this region.")

    def get_farming_practice(self, practice):
        return self.practices.get(practice, "No data available for this practice.")

    def get_market_access_info(self, info_type):
        return self.market_access.get(info_type, "No data available for this information.")

    def get_value_addition_idea(self, idea):
        return self.value_addition.get(idea, "No data available for this idea.")

def main():
    advisor = AgribusinessAdvisor()

    # User input for crop selection
    region = input("Enter your region (e.g., Rift Valley, Central Kenya, Meru): ")
    print(advisor.get_crop_selection(region))

    # User input for farming practice
    practice = input("Enter a farming practice (e.g., soil_health, pest_control, irrigation): ")
    print(advisor.get_farming_practice(practice))

    # User input for market access information
    info_type = input("Enter market access information type (e.g., find_buyers, pricing_trends): ")
    print(advisor.get_market_access_info(info_type))

    # User input for value addition idea
    idea = input("Enter a value addition idea (e.g., drying_fruits, packaging_honey): ")
    print(advisor.get_value_addition_idea(idea))

if __name__ == "__main__":
    main()