import tkinter as tk


def process_input():
    input_text = input_textbox.get("1.0", "end-1c")
    show_arrival = arrive_checkbox_var.get()
    show_attack = attack_checkbox_var.get()
    show_wall = wall_checkbox_var.get()
    show_noble = noble_checkbox_var.get()
    show_loyalty = loyalty_checkbox_var.get()
    output_text = process_instances(input_text, show_arrival, show_attack, show_wall, show_noble, show_loyalty)
    output_textbox.delete("1.0", "end")
    output_textbox.insert("1.0", output_text)

    output_textbox.tag_add("sel", "1.0", "end")
    output_textbox.clipboard_clear()
    output_textbox.clipboard_append(output_text)
    output_textbox.tag_remove("sel", "1.0", "end")
    output_textbox.update_idletasks()

    status_label.config(text="A formázott bejövők másolva a vágólapra, Ctrl + V-vel másolhatod be a fórumra!")


def process_instances(input_text, show_arrival, show_attack, show_wall, show_noble, show_loyalty):
    lines = input_text.split('\n')

    instances = []
    current_instance = []

    for line in lines:
        line = line.strip()
        if line.startswith("[b]Falu:[/b]"):
            if current_instance:
                instances.append(current_instance)
            current_instance = [line]
        else:
            current_instance.append(line)

    if current_instance:
        instances.append(current_instance)

    result = []

    for idx, instance in enumerate(instances, start=1):
        try:
            attack_count = 0
            noble_count = 0
            instance_info = []
            arrival_time = "N/A"

            for line in instance:
                instance_info.append(line)
                if line.startswith("[command]attack[/command] FN"):
                    noble_count += 1
                if line.startswith("[command]attack"):
                    attack_count += 1
                    arrive = line.split("ideje: ")
                    if len(arrive) > 1:
                        arrival_time = arrive[1]

            village_line = instance_info[0].replace('[b]Falu:[/b] ', '')
            wall = instance_info[1]
            loyalty = instance_info[2]

            output = f"{village_line}"

            if show_wall:
                output += f" | {wall}"

            if show_loyalty:
                output += f" | {loyalty}"

            if show_arrival:
                output += f" | [b]1. támadás: [color=#ff0000]{arrival_time}[/color][/b]"

            if show_attack:
                output += f" | [b]össz támadás [color=#ff0000]({attack_count})[/color][/b]"

            if show_noble:
                output += f" | [b]nemes [color=#ff0000]({noble_count})[/color][/b]"

            if idx % 5 is 0 and idx is not 1:
                output += f"\n-----------------------------------------------------------"

            result.append(f"[b]#{idx}[/b] | {output}")
        except:
            result.append(f"Valami hiba történt. Talán nem jót másoltál a bejövők közé")

    return '\n'.join(result)


root = tk.Tk()
root.title("Bejövő átalakító - készítette: Say Hi")

input_label = tk.Label(root, text="Bejövők:")
input_label.grid(row=0, column=0, columnspan=5)

input_textbox = tk.Text(root, height=10, width=120)
input_textbox.grid(row=1, column=0, columnspan=5)

wall_checkbox_var = tk.BooleanVar(value=True)
wall_checkbox = tk.Checkbutton(root, text="Fal", variable=wall_checkbox_var)
wall_checkbox.grid(row=2, column=0)

arrive_checkbox_var = tk.BooleanVar(value=True)
arrive_checkbox = tk.Checkbutton(root, text="Érkezés ideje", variable=arrive_checkbox_var)
arrive_checkbox.grid(row=2, column=1)

attack_checkbox_var = tk.BooleanVar(value=True)
attack_checkbox = tk.Checkbutton(root, text="Támadás db", variable=attack_checkbox_var)
attack_checkbox.grid(row=2, column=2)

noble_checkbox_var = tk.BooleanVar(value=True)
noble_checkbox = tk.Checkbutton(root, text="Nemes db", variable=noble_checkbox_var)
noble_checkbox.grid(row=2, column=3)

loyalty_checkbox_var = tk.BooleanVar(value=True)
loyalty_checkbox = tk.Checkbutton(root, text="Hűség", variable=loyalty_checkbox_var)
loyalty_checkbox.grid(row=2, column=4)

process_button = tk.Button(root, text="Átalakítás", command=process_input)
process_button.grid(row=3, column=0, columnspan=5)

output_label = tk.Label(root, text="Formázott bejövők:")
output_label.grid(row=4, column=0, columnspan=5)

output_textbox = tk.Text(root, height=10, width=120)
output_textbox.grid(row=5, column=0, columnspan=5)

status_label = tk.Label(root, text="", bg='#fff', fg='#f00')
status_label.grid(row=6, column=0, columnspan=5)

root.mainloop()
