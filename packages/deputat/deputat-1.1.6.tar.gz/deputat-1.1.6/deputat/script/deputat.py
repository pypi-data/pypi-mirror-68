import os
import pandas as pd
import json

from deputat import settings


def subjects(reverse=False):
    with open(settings.subs_json(), 'r') as jfile:
        subs = json.load(jfile)
    if reverse:
        return {short: long for long, short in subs.items()}
    return subs

def dump_subjects(subs: dict):
    with open(settings.subs_json(), 'w') as jfile:
        json.dump(subs, jfile)


save = settings.save_dir()


class Class:
    def __init__(self, level: int, name: str, subjects: dict):
        self.level = int(level)
        self.name = name
        self.subjects = subjects


    def __str__(self):
        return f'Klasse:\t {self.level}{self.name}\n' \
               f'Fächer:\t {self._get_subjects()}'

    def __gt__(self, other):
        if self.level == other.level:
            return self.name > other.name
        return self.level > other.level

    def __lt__(self, other):
        if self.level == other.level:
            return self.name < other.name
        return self.level < other.level

    def __eq__(self, other):
        return self.name == other.name and self.level == other.level

    def __repr__(self):
        return f'Class({self.level}, {self.name}, {self.subjects})'

    def list_it(self):
        return [self.level, self.name, ';'.join(self.subjects_to_list())]


    def subjects_to_list(self):
        liste = []
        for i in self.subjects:
            liste.append(str(i + f'-{self.subjects[i][0]}-{self.subjects[i][1]}'))
        return liste


    def _get_subjects(self):
        text = ''
        for i in self.subjects:
            text += i + f' ({self.subjects[i][0]} Stunden) bei {self.subjects[i][1]}\n\t\t '
        return text


    def get_fullname(self):
        return f'{self.level}{self.name}'


    def hours_missing(self):
        for i in self.subjects:
            if self.subjects[i][1] == 'null':
                return True
        return False


    def list_teachers(self):
        teachers = []
        for i in self.subjects:
            if self.subjects[i][1] not in teachers and self.subjects[i][1] != 'null':
                teachers.append(self.subjects[i][1])
        return teachers


class Teacher:
    def __init__(self, name: str, short: str, hours: int, subjects: list):
        assert hours >= 0, f'{name} hat weniger als 0 Stunden ({hours}).'
        self.name = name
        self.short = short
        self.hours = hours
        self.subjects = subjects
        self.hours_left = hours


    def __str__(self):
        subs = {}
        for s in self.subjects:
            s = subjects(True)[s]
            subs[s] = 0
        for c in AllClasses.classes:
            for s in c.subjects:
                if subjects(True)[s] in subs:
                    if c.subjects[s][1] == self.short:
                        subs[subjects(True)[s]] += int(c.subjects[s][0])
        text = f'Name:\t {self.name} ({self.short})\n' \
               f'Fächer:\t {_build_string_from_dict(subs)}\n' \
               f'Stunden: {self.hours} ({self._get_hours_left()}h übrig)'
        return text


    def __repr__(self):
        return f'Teacher({self.name}, {self.short}, {self.hours}, {self.subjects})'


    def __eq__(self, other):
        return self.name == other.name and self.short == other.short


    def __lt__(self, other):
        return self.short < other.short


    def __gt__(self, other):
        return self.short > other.short


    def list_it(self):
        return [self.name, self.short, str(self.hours), ';'.join(self.subjects)]


    def _get_hours_left(self):
        teached_hours = []
        for c in AllClasses.classes:
            for s in c.subjects:
                if c.subjects[s][1] == self.short:
                    teached_hours.append(int(c.subjects[s][0]))
        return self.hours - sum(teached_hours)


class AllTeachers:
    teachers = []
    backup = []
    filename = 'lehrer.td'

    def read_data(self, path, file=None):
        if file:
            path, file = os.path.split(path)
            liste = read_data(path, 'td', file)
        else:
            liste = read_data(path, 'td')
        for i in liste:
            self.add_teacher(i)


    def save_data(self, location=save):
        return save_data(self.filename, location)


    def _list_teacher_hours(self):
        list = []
        for t in self.teachers:
            subs = {}
            for s in t.subjects:
                subs[s] = 0
            for c in AllClasses.classes:
                for s in c.subjects:
                    if s in subs:
                        if c.subjects[s][1] == t.short:
                            subs[s] += int(c.subjects[s][0])
            list.append(f'{t.name}\t({t.short})\t-\t[{_build_string_from_dict(subs)}]')
        return list


    def add_teacher(self, teacher=None, name=None, short=None, hours=None, subjects=None):
        if not teacher:
            teacher = Teacher(name, short, hours, subjects)
        if teacher in self.teachers:
            return False
        self.teachers.append(teacher)
        return True


    def get_all_teachers(self) -> list:
        liste = []
        for t in self.teachers:
            if t.short not in liste:
                liste.append(t.short)
        return liste


class AllClasses:
    classes = []
    backup = []
    filename = 'klassen.cd'

    def read_data(self, path, file=None):
        if file:
            path, file = os.path.split(path)
            liste = read_data(path, 'cd', file)
        else:
            liste = read_data(path, 'cd')
        for i in liste:
            self.add_class(i)


    def save_data(self, location=save):
        return save_data(self.filename, location)


    def list_levels(self):
        liste = []
        for c in self.classes:
            if str(c.level) not in liste:
                liste.append(str(c.level))
        return liste


    def add_class(self, klasse=None, level=None, name=None, subjects=None):
        if not klasse:
            klasse = Class(level, name, subjects)
        if klasse in self.classes:
            return False
        self.classes.append(klasse)
        return True


    def get_all_subjects(self) -> list:
        list = []
        for c in self.classes:
            for s in c.subjects:
                if s not in list:
                    list.append(s)
        return list


    def get_all_classes(self) -> list:
        liste = []
        for c in self.classes:
            if c.get_fullname() not in liste:
                liste.append(c.get_fullname())
        return liste


def _build_string_from_dict(subs: dict):
    text = ""
    for i in subs:
        text += f'{i}: {subs[i]}h, '
    return text[0:-2]


def read_data(path, typ, filename=None):
    liste = []
    if filename:
        if typ == 'cd':
            with open(os.path.join(path, filename), 'r') as file:
                lines = file.readlines()[1:]
            for line in lines:
                line = line.strip().split(',')
                line[-1] = line[-1].split(';')  # 'S-2-null'
                new = {}
                for fach in line[-1]:
                    fach = fach.split('-')  # ['S', '2', 'null']
                    fach[1] = int(fach[1])
                    new[fach[0]] = fach[1:]
                line[-1] = new
                liste.append(build_object(line, typ))
        elif typ == 'td':
            with open(os.path.join(path, filename), 'r') as file:
                lines = file.readlines()[1:]
            for line in lines:
                line = line.strip().split(',')
                line[-1] = line[-1].split(';')
                liste.append(build_object(line, typ))
    for f in os.listdir(path):
        if typ == 'cd':
            if f.endswith('.cd'):
                with open(os.path.join(path, f), 'r') as file:
                    lines = file.readlines()[1:]
                for line in lines:
                    line = line.strip().split(',')
                    line[-1] = line[-1].split(';')  # 'S-2-null'
                    new = {}
                    for fach in line[-1]:
                        fach = fach.split('-')  # ['S', '2', 'null']
                        fach[1] = int(fach[1])
                        new[fach[0]] = fach[1:]
                    line[-1] = new
                    liste.append(build_object(line, typ))
        elif typ == 'td':
            if f.endswith('.td'):
                with open(os.path.join(path, f), 'r') as file:
                    lines = file.readlines()[1:]
                for line in lines:
                    line = line.strip().split(',')
                    line[-1] = line[-1].split(';')
                    liste.append(build_object(line, typ))
    return liste


def build_object(line: list, typ: str) -> bool:
    if typ == 'td':
        name, short, hours, subjects = line[0], line[1], int(line[2]), line[3]
        return Teacher(name, short, hours, subjects)
    elif typ == 'cd':
        level, name, subjects = line[0], line[1], line[2]
        return Class(level, name, subjects)


def save_data(filename, path=save):
    path = os.path.join(path, filename)
    try:
        file = open(path, 'w')
        if filename.endswith('.td'):
            print('name,kürzel,stunden,fächer', file=file)
            for obj in AllTeachers.teachers:
                print(",".join(obj.list_it()), file=file)
        elif filename.endswith('.cd'):
            print('klassenstufe,name,fächer(fach-stundenzahl-lehrer)', file=file)
            for obj in AllClasses.classes:
                print(",".join([str(i) for i in obj.list_it()]), file=file)
        file.close()
        return True
    except TypeError as error:
        print(error)
        return False


def pretty_out_teachers(classes: AllClasses, teachers: AllTeachers):
    s_dict = {'Fächer': sorted(classes.get_all_subjects())}
    teachers_list = sorted(teachers.get_all_teachers())
    ret_df = pd.DataFrame(s_dict)
    t_dict = {}
    for t in sorted(teachers.teachers):
        infos = get_teachers_classes(classes, t)
        infos_list = sorted(infos)
        subs = [infos[i] for i in infos_list]
        subs = [f'{format_subs(i)}' for i in subs]
        t_dict[t.short] = subs
    for i in t_dict:
        ret_df[i] = t_dict[i]
    return ret_df


def format_subs(xs: list) -> str:
    hours = ''
    classes = ''
    if xs[0] == 0:
        return ''
    return f'{str(xs[0])} - {xs[1][:-2]}'


def pretty_out_classes(classes: AllClasses):
    all_subs = sorted(classes.get_all_subjects())
    s_dict = {'Fächer': all_subs}
    ret_df = pd.DataFrame(s_dict)
    c_dict = {}
    for c in sorted(classes.classes):
        info_dict = {}
        for s in all_subs:
            info_dict[s] = [0, 'null']
        for s in info_dict:
            if s in c.subjects:
                info_dict[s] = c.subjects[s]
        infos_list = sorted(info_dict)
        infos = [info_dict[i] for i in infos_list]
        infos = [f'{format_info(i)}' for i in infos]
        c_dict[c.get_fullname()] = infos
    for i in c_dict:
        ret_df[i] = c_dict[i]
    return ret_df


def format_info(xs: list) -> str:
    if xs[0] == 0:
        return ''
    return f'{xs[0]} - {xs[1]}'


def get_teachers_classes(classes: AllClasses, teacher: Teacher):
    ret_dict = {}
    for s in sorted(classes.get_all_subjects()):
        ret_dict[s] = [0, '']
    for c in sorted(classes.classes):
        for s in c.subjects:
            if c.subjects[s][1] == teacher.short:
                ret_dict[s][0] += c.subjects[s][0]
                ret_dict[s][1] += f'{c.get_fullname()}, '
    return ret_dict


if __name__ == '__main__':
    t = AllTeachers()
    t.read_data('/home/lfreist/Documents/projects/deputat/deputat/data')
    c = AllClasses()
    c.read_data('/home/lfreist/Documents/projects/deputat/deputat/data')