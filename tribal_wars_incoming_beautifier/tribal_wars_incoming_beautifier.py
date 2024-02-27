import tkinter as tk


def process_input():
    input_text = input_textbox.get('1.0', 'end-1c')
    show_arrival = arrive_checkbox_var.get()
    show_attack = attack_checkbox_var.get()
    show_wall = wall_checkbox_var.get()
    show_noble = noble_checkbox_var.get()
    show_loyalty = loyalty_checkbox_var.get()
    output_text = process_instances(input_text, show_arrival, show_attack, show_wall, show_noble, show_loyalty)
    output_textbox.delete('1.0', 'end')
    output_textbox.insert('1.0', output_text)

    output_textbox.tag_add('sel', '1.0', 'end')
    output_textbox.clipboard_clear()
    output_textbox.clipboard_append(output_text)
    output_textbox.tag_remove('sel', '1.0', 'end')
    output_textbox.update_idletasks()

    status_label.config(text='A formázott bejövők másolva a vágólapra, Ctrl + V-vel másolhatod be a fórumra!')


def format_noble_incomings(noble_incoming):
    split_noble = noble_incoming.split('ideje: ')
    temp_noble = split_noble[1].split(' [player]')
    date = temp_noble[0].replace(',', '').replace('.', '').replace(':', ' ').split()
    return dict(
        month=date[0],
        day=date[1],
        year=date[2],
        hour=date[3],
        minute=date[4],
        second=date[5],
        ms=date[6],
        snipe=False)


def check_train_snipe_possibility(nobles):
    for noble in range(len(nobles) - 1):
        current_ms = int(nobles[noble]['ms'])
        next_ms = int(nobles[noble + 1]['ms'])
        if abs(current_ms - next_ms) == int(noble_interval_var.get()):
            nobles[noble]['snipe'] = True
            nobles[noble + 1]['snipe'] = True


def process_instances(input_text, show_arrival, show_attack, show_wall, show_noble, show_loyalty):
    lines = input_text.split('\n')

    instances = []
    current_instance = []

    for line in lines:
        line = line.strip()
        if line.startswith('[b]Falu:[/b]'):
            if current_instance:
                instances.append(current_instance)
            current_instance = [line]
        elif line:
            current_instance.append(line)

    if current_instance:
        instances.append(current_instance)

    result = []

    for idx, instance in enumerate(instances, start=1):
        try:
            attack_count = 0
            instance_info = []
            arrival_times = []
            nobles = []

            for line in instance:
                instance_info.append(line)
                if line.startswith('[command]attack[/command] FN'):
                    noble_attack = format_noble_incomings(line)
                    nobles.append(noble_attack)
                if line.startswith('[command]attack'):
                    attack_count += 1
                    arrive = line.split('ideje: ')
                    if len(arrive) > 1:
                        arrival_times.append(arrive[1])

            village_line = instance_info[0].replace('[b]Falu:[/b] ', '')
            wall = instance_info[1].replace('Falszint', 'Fal')
            loyalty = instance_info[2].replace('[b]Hűség:[/b] ', '') + '%'

            output = f'{village_line}'

            if show_wall:
                output += f' | {wall}'

            if show_loyalty:
                output += f' | [b]{loyalty}[/b]'

            if show_arrival and arrival_times:
                arrival_time = arrival_times[0]
                output += f' | [b]1. támadás: [color=#ff0000]{arrival_time}[/color][/b]'

            if show_attack:
                output += f' | [b]össz támadás [color=#ff0000]({attack_count})[/color][/b]'

            if show_noble:
                check_train_snipe_possibility(nobles)
                if any(entry.get('snipe', False) for entry in nobles):
                    color = '#00a500'
                    output += f'\n[b][color={color}]---------- VÁGHATÓ NEMESEK ----------[/color][/b]'
                for noble in range(0, len(nobles)):
                    incoming = nobles[noble]
                    if incoming['snipe']:
                        color = '#00a500'
                    else:
                        color = '#ff0000'
                    output += f'\n[b]-----------> {noble + 1}. nemes érkezik: [color={color}]{incoming["year"]}.{incoming["month"]}.{incoming["day"]} {incoming["hour"]}:{incoming["minute"]}:{incoming["second"]}.{incoming["ms"]}[/color][/b]'

            if idx % 5 == 0 and idx != 1:
                output += f'\n-----------------------------------------------------------'

            result.append(f'[b]#{idx}[/b] | {output}')

        except Exception as ex:
            print(ex)
            result.append(f'Valami hiba történt. Talán nem jót másoltál a bejövők közé')

    return '\n'.join(result)


root = tk.Tk()
root.title('Bejövő átalakító - készítette: Say Hi')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

input_label = tk.Label(root, text='Bejövők:')
input_label.grid(row=0, column=0, columnspan=5, sticky='nsew')

input_textbox = tk.Text(root, height=10, width=120)
input_textbox.grid(row=1, column=0, columnspan=5, sticky='nsew')

checkbox_frame = tk.Frame(root)
checkbox_frame.grid(row=2, column=0, columnspan=5, sticky='nsew')
checkbox_frame.grid_columnconfigure(0, weight=1)
checkbox_frame.grid_columnconfigure(1, weight=1)
checkbox_frame.grid_columnconfigure(2, weight=1)
checkbox_frame.grid_columnconfigure(3, weight=1)
checkbox_frame.grid_columnconfigure(4, weight=1)

wall_checkbox_var = tk.BooleanVar(value=True)
wall_checkbox = tk.Checkbutton(checkbox_frame, text='Fal', variable=wall_checkbox_var)
wall_checkbox.grid(row=0, column=0)

arrive_checkbox_var = tk.BooleanVar(value=True)
arrive_checkbox = tk.Checkbutton(checkbox_frame, text='Érkezés ideje', variable=arrive_checkbox_var)
arrive_checkbox.grid(row=0, column=1)

attack_checkbox_var = tk.BooleanVar(value=True)
attack_checkbox = tk.Checkbutton(checkbox_frame, text='Támadás db', variable=attack_checkbox_var)
attack_checkbox.grid(row=0, column=2)

noble_checkbox_var = tk.BooleanVar(value=True)
noble_checkbox = tk.Checkbutton(checkbox_frame, text='Nemes részletezés', variable=noble_checkbox_var)
noble_checkbox.grid(row=0, column=3)

loyalty_checkbox_var = tk.BooleanVar(value=True)
loyalty_checkbox = tk.Checkbutton(checkbox_frame, text='Hűség', variable=loyalty_checkbox_var)
loyalty_checkbox.grid(row=0, column=4)

options = ['50', '100', '150', '200']

noble_interval_label = tk.Label(checkbox_frame, text='Nemesek közti minimum ms:')
noble_interval_label.grid(row=0, column=5)

noble_interval_var = tk.StringVar(checkbox_frame)
noble_interval_var.set(options[1])

max_option_length = max(len(option) for option in options)
dropdown_width = max_option_length + 2

noble_interval_dropdown = tk.OptionMenu(checkbox_frame, noble_interval_var, *options)
noble_interval_dropdown.config(width=dropdown_width)
noble_interval_dropdown.grid(row=0, column=6)

process_button = tk.Button(root, text='Átalakítás', command=process_input)
process_button.grid(row=3, column=0, columnspan=5)

output_label = tk.Label(root, text='Formázott bejövők:')
output_label.grid(row=4, column=0, columnspan=5, sticky='nsew')

output_textbox = tk.Text(root, height=10, width=120)
output_textbox.grid(row=5, column=0, columnspan=5, sticky='nsew')

status_label = tk.Label(root, text='', bg='#fff', fg='#f00')
status_label.grid(row=6, column=0, columnspan=5, sticky='nsew')

for i in range(5):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
