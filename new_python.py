weight=input("Enter your weight in pound: ")
weight_in_kg=int(weight)*0.45359237154
print("Your weight in kilogram is: ",weight_in_kg)

"""Simple BMI calculator and weight converter.

This script accepts weight and height in a few common units, computes BMI,
and prints the BMI value and WHO category.
"""

def pounds_to_kg(pounds: float) -> float:
	return pounds * 0.45359237


def calculate_bmi(weight: float, height: float, weight_unit: str = "kg", height_unit: str = "m") -> float:
	"""Calculate BMI given weight and height with units.

	weight_unit: 'kg' or 'lb'
	height_unit: 'm' (meters)
	"""
	w_kg = weight if weight_unit == "kg" else pounds_to_kg(weight)
	h_m = height
	# if caller passed cm, convert to m
	if height_unit == "cm":
		h_m = height / 100.0
	# Note: if height_unit == 'm' we already use meters
	if h_m <= 0:
		raise ValueError("Height must be positive")
	bmi = w_kg / (h_m ** 2)
	return bmi


def bmi_category(bmi: float) -> str:
	if bmi < 18.5:
		return "Underweight"
	if bmi < 25.0:
		return "Normal weight"
	if bmi < 30.0:
		return "Overweight"
	return "Obesity"


def prompt_float(prompt: str) -> float:
	while True:
		val = input(prompt).strip()
		try:
			return float(val)
		except ValueError:
			print("Please enter a valid number.")


def main():
	print("BMI Calculator")
	weight = prompt_float("Enter your weight (number): ")
	wu = input("Is that in kilograms or pounds? [kg/lb] ").strip().lower()
	if wu not in ("kg", "lb"):
		print("Unknown unit, assuming kilograms.")
		wu = "kg"

	# Height input: support meters, centimeters or feet+inches
	hu = input("Height unit - meters, centimeters, or feet? [m/cm/ft] ").strip().lower()
	if hu == "ft":
		feet = prompt_float("Feet: ")
		inches = prompt_float("Inches: ")
		total_inches = feet * 12 + inches
		# 1 inch = 0.0254 m
		height_m = total_inches * 0.0254
		bmi = calculate_bmi(weight, height_m, weight_unit=wu, height_unit="m")
	else:
		h = prompt_float("Enter your height (number): ")
		if hu not in ("m", "cm"):
			print("Unknown height unit, assuming meters.")
			hu = "m"
		bmi = calculate_bmi(weight, h, weight_unit=wu, height_unit=hu)

	print(f"Your BMI is: {bmi:.1f}")
	print("Category:", bmi_category(bmi))


if __name__ == "__main__":
	main()

