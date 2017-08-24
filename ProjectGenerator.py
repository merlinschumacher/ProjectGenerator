import os
from pathlib import Path
import string

class ProjectTemplate:
    def __init__(self,ProjectType):
        self.ProjectFileLocation = Path('templates/' + ProjectType + '.project/Projectfile')
        self.ProjectFile = []
        with self.ProjectFileLocation.open() as ProjectFileContent:
            for Line in ProjectFileContent:
                self.ProjectFile.append(Line)

    def ProcessProjectFile(self):
        for CommandLine in self.ProjectFile:
            CommandProcessor(CommandLine)

def CommandProcessor(CommandLine):
    KnownCommands = ['LABEL', 'DIR', 'COPY', 'FILE', 'CMD', 'LINK', 'APP', 'ECHO']
    SplitCommand = CommandLine.split(" ",1)
    if (SplitCommand[0] in KnownCommands):
        Command = SplitCommand[0]
        Parameters = SplitCommand[1]

        if (Command == 'LABEL'):
            SplitParameters=Parameters.split("=", 1)
            LabelType = SplitParameters[0]
            LabelValue = SplitParameters[1]
            print(LabelType + ": " + LabelValue)
        elif (Command == 'DIR'):
            FilledParameters = Parameters.format(BASEDIR='target',TITLE='MeinProjekt')
            if not os.path.exists(FilledParameters):
                os.makedirs(FilledParameters)

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

GenerateProject = ProjectTemplate('Python')
GenerateProject.ProcessProjectFile()