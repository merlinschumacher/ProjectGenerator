import os
import shutil
from pathlib import Path

GlobalProjectFolder = str(Path.home()) + "Projects/"

class ProjectTemplate:
    def __init__(self,ProjectType):
        self.ProjectFileLocation = Path('templates/' + ProjectType + '.project/Projectfile')
        self.ProjectFile = []
        self.ProjectBaseDirectory = str(GlobalProjectFolder + ProjectTitle)
        self.CommandList = []
        with self.ProjectFileLocation.open() as ProjectFileContent:
            for Line in ProjectFileContent:
                self.ProjectFile.append(Line)


def CommandProcessor(ProjectTemplate):
    for CommandLine in ProjectTemplate.ProjectFile:
        KnownCommands = ['LABEL', 'DIR', 'COPY', 'FILE', 'CMD', 'LINK', 'ECHO']
        SplitCommand = CommandLine.split(" ", 1)
        if (SplitCommand[0] in KnownCommands):
            Command = SplitCommand[0]
            Parameters = str(SplitCommand[1])

            if (Command == 'LABEL'):
                SplitParameters = Parameters.split("=", 1)
                LabelType = SplitParameters[0]
                LabelValue = SplitParameters[1]

                print(LabelType + ": " + LabelValue)

            elif (Command == 'DIR'):
                FilledParameters = str(Parameters.format(TITLE='MeinProjekt'))
                if not os.path.exists(ProjectTemplate.ProjectBaseDirectory + FilledParameters):
                    os.makedirs(FilledParameters)

            elif (Command == 'COPY'):
                SplitParameters = Parameters.split(" ")
                shutil.copy2(str(SplitParameters[0]), ProjectTemplate.ProjectBaseDirectory + str(SplitParameters[1]))

            elif (Command == 'FILE'):
                open(ProjectTemplate.ProjectBaseDirectory + Parameters, 'a').close()

            elif (Command == 'CMD'):
                cur_dir = os.path.abspath(".")
                os.chdir(ProjectTemplate.ProjectBaseDirectory)
                os.system(str(Parameters))
                os.chdir(curdir)

            elif (Command == 'LINK'):
                cur_dir = os.path.abspath(".")
                os.chdir(ProjectTemplate.ProjectBaseDirectory)
                os.symlink(ProjectTemplate.ProjectBaseDirectory + str(SplitParameters[0]),
                           ProjectTemplate.ProjectBaseDirectory + str(SplitParameters[1]))
                os.chdir(curdir)

            elif (Command == 'ECHO'):
                print(Parameters)


def GetTemplateList():
    TemplateList = []
    TemplatePath = Path('templates')
    for Directory in TemplatePath.iterdir():
        if (Directory.is_dir()) and (str(Directory.name).lower().endswith("project")):
            ProjectType = str(Directory.name).replace(".project", "")
            ProjectFile = Directory / 'Projectfile'
            if (ProjectFile.exists()):
                TemplateList.append(ProjectType)

    return TemplateList


ProjectTitle = input("Enter a title for your project: ")
GenerateProject = ProjectTemplate('Python')
CommandProcessor(GenerateProject)
