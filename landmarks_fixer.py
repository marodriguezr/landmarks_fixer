import turtle
import numpy as np
import patch_turtle_image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import tooltip as tt

class App:
    def __init__(self) -> None:
        self.initScreen()
        self.initMenus()
        self.initCanvas()
        self.initTurtleScreen()
        self.initButtons()
        self.initStatusLabel()
        self.loadActions()

    def initScreen(self):
        self.screen = tk.Tk()
        self.screen.title("Corrector de landmarks")

    def initMenus(self):
        self.menu = tk.Menu(self.screen)
        self.screen.config(menu=self.menu)

        self.fileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Archivo", menu=self.fileMenu)
        self.fileMenu.add_command(
            label="Abrir archivo de puntos (*.pts)", accelerator="( 1 )  ( N )", command=self.loadFile)
        self.fileMenu.add_command(
            label="Abrir directorio de archivos de puntos (*.pts)", accelerator="( 2 )  ( M )",command=self.loadFilesDirectory)

        self.helpMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Ayuda", menu=self.helpMenu)
        self.helpMenu.add_command(label="Mostrar controles de teclado", command=lambda: messagebox.showinfo(title="Controles de teclado", message="W\t^\t\tArriba" + "\n" + "A\t<\t\tIzquierda" + "\n" + "S\tv\t\tAbajo" + "\n" + "D\t>\t\tDerecha" +
                                  "\n" + "+\t\t\tAvanzar punto" + "\n" + "-\t\t\tRetroceder punto" + "\n" + "E\t\t\tAvanzar imagen" + "\n" + "Q\t\t\tRetroceder imagen" + "\n" + "Espacio\tG\t\tGuardar\nH\tC\t\tDeshacer cambios" + "\n" + "1\tN\t\tNuevo archivo" + "\n" + "M\t2\t\tNuevo directorio"))
        self.helpMenu.add_command(label="Acerca de", command=lambda: messagebox.showinfo(
            title="Acerca de", message="Desarrollado por:\n\nMontalvo Steven\nNavarrete Danny\nQuilca Freddy\nRodríguez Miguel\nUlcuango Lenin"))

    def initCanvas(self):
        self.canvas = tk.Canvas(self.screen, width=640, height=480)
        self.canvas.grid(row=0, column=0, columnspan=7)

    def initTurtleScreen(self):
        self.turtleScreen = turtle.TurtleScreen(self.canvas)
        self.turtleScreen.setworldcoordinates(0, 0, 640, 480)

    def initButtons(self):
        self.btnBackwardImage = tk.Button(
            text="<< Retroceder imagen", command=self.imageBackward)
        self.btnBackwardImage.grid(row=1, column=0)
        tt.CreateToolTip(self.btnBackwardImage, text="( Q )")

        self.btnLoadFile = tk.Button(
            text="Abrir archivo", command=self.loadFile)
        self.btnLoadFile.grid(row=2, column=0)
        tt.CreateToolTip(self.btnLoadFile, text="( 1 )\t( N )")

        self.btnBackward = tk.Button(
            text="- Retroceder punto", command=self.forma_regresar)
        self.btnBackward.grid(row=1, column=1)
        tt.CreateToolTip(self.btnBackward, text="( - )")

        self.btnDetachChanges = tk.Button(
            text="Deshechar cambios", command=self.detachChanges)
        self.btnDetachChanges.grid(row=2, column=1)
        tt.CreateToolTip(self.btnDetachChanges, text="( C )\t( H )")

        self.btnLeft = tk.Button(text="<", command=self.izquierda)
        self.btnLeft.grid(row=2, column=2)
        tt.CreateToolTip(self.btnLeft, text="( A )\t( < )")

        self.btnUp = tk.Button(text="^", command=self.arriba)
        self.btnUp.grid(row=1, column=3)
        tt.CreateToolTip(self.btnUp, text="( W )\t( ^ )")

        self.btnDown = tk.Button(text="v", command=self.abajo)
        self.btnDown.grid(row=2, column=3)
        tt.CreateToolTip(self.btnDown, text="( S )\t( v )")

        self.btnRight = tk.Button(text=">", command=self.derecha)
        self.btnRight.grid(row=2, column=4)
        tt.CreateToolTip(self.btnRight, text="( D )\t( > )")

        self.btnForward = tk.Button(
            text="Avanzar punto +", command=self.forma_avanzar)
        self.btnForward.grid(row=1, column=5)
        tt.CreateToolTip(self.btnForward, text="( + )")

        self.btnSaveChanges = tk.Button(
            text="Guardar cambios", command=self.guardar)
        self.btnSaveChanges.grid(row=2, column=5)
        tt.CreateToolTip(self.btnSaveChanges, text="( Espacio )\t( G )")

        self.btnForwardImage = tk.Button(
            text="Avanzar imagen >>", command=self.imageForward)
        self.btnForwardImage.grid(row=1, column=6)
        tt.CreateToolTip(self.btnForwardImage, text="( E )")

        self.btnLoadFolder = tk.Button(
            text="Abrir directorio", command=self.loadFilesDirectory)
        self.btnLoadFolder.grid(row=2, column=6)
        tt.CreateToolTip(self.btnLoadFolder, text="( 2 )")

        self.disableDirectoryButtons()
        self.disableWorkspaceButtons()

    def initStatusLabel(self):
        self.lblStatus = tk.Label(
            master=self.screen, text="A la espera de interacción", bd=1, relief=tk.SUNKEN, anchor=tk.E, bg="lightblue")
        self.lblStatus.grid(row=3, column=0, columnspan=7, sticky=tk.W+tk.E)

    def initConstants(self):
        self.activeTurtleIndex = -1
        self.turtles = []
        self.ptsCoordinates = []

    def loadActions(self):
        self.turtleScreen.listen()
        self.turtleScreen.onkeypress(self.loadFile, "1")
        self.turtleScreen.onkeypress(self.loadFile, "n")
        self.turtleScreen.onkeypress(self.loadFilesDirectory, "2")
        self.turtleScreen.onkeypress(self.loadFilesDirectory, "m")

    def loadWorkspaceActions(self):
        self.turtleScreen.onkeypress(self.arriba, "w")
        self.turtleScreen.onkeypress(self.abajo, "s")
        self.turtleScreen.onkeypress(self.izquierda, "a")
        self.turtleScreen.onkeypress(self.derecha, "d")
        self.turtleScreen.onkeypress(self.arriba, "Up")
        self.turtleScreen.onkeypress(self.abajo, "Down")
        self.turtleScreen.onkeypress(self.izquierda, "Left")
        self.turtleScreen.onkeypress(self.derecha, "Right")
        self.turtleScreen.onkeypress(self.forma_avanzar, "+")
        self.turtleScreen.onkeypress(self.forma_regresar, "-")
        self.turtleScreen.onkeypress(self.guardar, "space")
        self.turtleScreen.onkeypress(self.guardar, "g")
        self.turtleScreen.onkeypress(self.detachChanges, "c")
        self.turtleScreen.onkeypress(self.detachChanges, "h")

    def loadDirectoryActions(self):
        self.turtleScreen.onkeypress(self.imageForward, "e")
        self.turtleScreen.onkeypress(self.imageBackward, "q")

    def loadFilesDirectory(self):
        try:
            self.lblStatus.config(
                text="Apertura de directorio en proceso", bg="lightblue")
            self.filesDirectory = filedialog.askdirectory()
            self.fileNames = []
            for fileName in os.listdir(self.filesDirectory):
                if (fileName.endswith(".pts")):
                    self.fileNames.append(fileName)
            if (len(self.fileNames) == 0):
                self.lblStatus.config(
                    text="Directorio seleccionado vacío", bg="#FED8B1")
                messagebox.showerror(
                    title="Directorio vacío", message="El directorio seleccionado no contiene archivos .pts, por favor seleccione un directorio válido")
            else:
                self.lblStatus.config(
                    text="Carga de archivos exitosa", bg="lightgreen")
                self.filePath = self.filesDirectory + "/" + self.fileNames[0]
                self.loadWorkspace()
                self.currentImageIndex = 0
            self.activeDirectoryButtons()
            self.activeWorkspaceButtons()
            self.loadDirectoryActions()
            self.loadWorkspaceActions()
        except:
            self.turtleScreen.clear()
            self.disableDirectoryButtons()
            self.disableWorkspaceButtons()
            self.loadActions()
            self.lblStatus.config(
                text="Apertura de directorio abortada.", bg="#FED8B1")

    def loadFile(self):
        try:
            self.filesDirectory = ""
            self.lblStatus.config(
                text="Apertura de archivo en proceso", bg="lightblue")
            self.filePath = filedialog.askopenfilename(
                title="Seleccione un archivo de puntos",
                filetypes=(("Archivo de puntos", "*.pts"),),
            )
            self.loadWorkspace()
            self.activeWorkspaceButtons()
            self.disableDirectoryButtons()
            self.loadWorkspaceActions()
        except Exception as e:
            self.turtleScreen.clear()
            self.disableDirectoryButtons()
            self.disableWorkspaceButtons()
            self.loadActions()
            self.lblStatus.config(
                text=str(e), bg="#FED8B1")

    def updateTitle(self):
        if (self.filePath != ""):
            self.screen.title(str(self.filePath))
        else:
            self.screen.title("Corrector de landmarks")

    def disableWorkspaceButtons(self):
        self.btnBackward.config(state="disabled")
        self.btnLeft.config(state="disabled")
        self.btnUp.config(state="disabled")
        self.btnDown.config(state="disabled")
        self.btnRight.config(state="disabled")
        self.btnForward.config(state="disabled")
        self.btnSaveChanges.config(state="disabled")
        self.btnDetachChanges.config(state="disabled")

    def activeWorkspaceButtons(self):
        self.btnBackward.config(state="active")
        self.btnLeft.config(state="active")
        self.btnUp.config(state="active")
        self.btnDown.config(state="active")
        self.btnRight.config(state="active")
        self.btnForward.config(state="active")
        self.btnSaveChanges.config(state="active")
        self.btnDetachChanges.config(state="active")

    def disableDirectoryButtons(self):
        self.btnBackwardImage.config(state="disabled")
        self.btnForwardImage.config(state="disabled")

    def activeDirectoryButtons(self):
        self.btnBackwardImage.config(state="active")
        self.btnForwardImage.config(state="active")

    def imageBackward(self):
        try:
            if (self.currentImageIndex > 0):
                self.filePath = self.filesDirectory + "/" + \
                    self.fileNames[self.currentImageIndex - 1]
                self.loadWorkspace()
                self.currentImageIndex = self.currentImageIndex - 1
                self.loadWorkspaceActions()
                self.loadDirectoryActions()
            else:
                self.lblStatus.config(
                    text="Archivo inicial alcanzado.", bg="#FED8B1")
        except:
            self.lblStatus.config(
                text="Retroceso de archivo abortado.", bg="#FED8B1")

    def imageForward(self):
        try:
            if (self.currentImageIndex < len(self.fileNames)-1):
                self.filePath = self.filesDirectory + "/" + \
                    self.fileNames[self.currentImageIndex + 1]
                self.loadWorkspace()
                self.currentImageIndex = self.currentImageIndex + 1
                self.loadWorkspaceActions()
                self.loadDirectoryActions()
            else:
                self.lblStatus.config(
                    text="Archivo final alcanzado.", bg="#FED8B1")
        except:
            self.lblStatus.config(
                text="Avance de archivo abortado.", bg="#FED8B1")

    def loadPtsFile(self):
        try:
            self.lblStatus.config(
                text="Carga de archivo de puntos en proceso", bg="lightblue")
            self.ptsCoordinates = np.loadtxt(self.filePath, comments=(
                "version:", "n_points:", "{", "}"))
            self.lblStatus.config(
                text="Carga de archivo de puntos exitosa", bg="lightgreen")
        except:
            raise Exception("Carga de archivo abortada.")

    def loadImageBackground(self):
        self.lblStatus.config(
            text="Carga de imagen en proceso", bg="lightblue")
        self.backgroundTurtle = turtle.RawTurtle(self.turtleScreen)
        self.backgroundTurtle.speed(0)
        self.backgroundTurtle.penup()
        self.backgroundTurtle.goto(0, 0)
        self.backgroundTurtle.setx(320)
        self.backgroundTurtle.sety(240)
        try:
            imagePath = str(self.filePath).replace(".pts", ".jpg")
            self.turtleScreen.register_shape(imagePath)
            self.backgroundTurtle.shape(imagePath)
            self.lblStatus.config(
                text="Carga de imagen exitosa", bg="lightgreen")
        except:
            raise Exception("Carga de imagen abortada.")

    def forma_avanzar(self):
        try:
            self.activeTurtleIndex += 1
            if self.activeTurtleIndex > 67:
                self.activeTurtleIndex = 0
            self.turtles[self.activeTurtleIndex].color("red")
            self.turtles[self.activeTurtleIndex].turtlesize(0.15, 0.15, 0.15)

            self.turtles[self.activeTurtleIndex - 1].color("green")
            self.turtles[self.activeTurtleIndex -
                         1].turtlesize(0.15, 0.15, 0.15)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Avance de punto abortado.", bg="#FED8B1")

    def forma_regresar(self):
        try:
            self.activeTurtleIndex -= 1
            if self.activeTurtleIndex < 0:
                self.activeTurtleIndex = 67
            self.turtles[self.activeTurtleIndex].color("red")
            self.turtles[self.activeTurtleIndex].turtlesize(0.15, 0.15, 0.15)

            self.turtles[0 if self.activeTurtleIndex ==
                         67 else self.activeTurtleIndex + 1].color("green")
            self.turtles[0 if self.activeTurtleIndex ==
                         67 else self.activeTurtleIndex + 1].turtlesize(0.15, 0.15, 0.15)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Retroceso de punto abortado.", bg="#FED8B1")

    def arriba(self):
        try:
            y = self.turtles[self.activeTurtleIndex].ycor()
            self.turtles[self.activeTurtleIndex].sety(y + 1)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Reposicionamiento del punto abortado.", bg="#FED8B1")

    def abajo(self):
        try:
            y = self.turtles[self.activeTurtleIndex].ycor()
            self.turtles[self.activeTurtleIndex].sety(y - 1)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Reposicionamiento del punto abortado.", bg="#FED8B1")

    def izquierda(self):
        try:
            x = self.turtles[self.activeTurtleIndex].xcor()
            self.turtles[self.activeTurtleIndex].setx(x - 1)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Reposicionamiento del punto abortado.", bg="#FED8B1")

    def derecha(self):
        try:
            x = self.turtles[self.activeTurtleIndex].xcor()
            self.turtles[self.activeTurtleIndex].setx(x + 1)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Reposicionamiento del punto abortado.", bg="#FED8B1")

    def guardar(self):
        try:
            self.lblStatus.config(
                text="Guardado de archivo en proceso", bg="lightblue")
            inicio = "version: 1\nn_points: 68\n{\n"
            contenido = ""
            for i in self.turtles:
                contenido = (
                    contenido + str(int(i.xcor())) + " " +
                    str(abs(int(i.ycor() - 480))) + "\n"
                )

            fin = "}"
            archivo = open(self.filePath, "w")
            archivo.write(inicio + contenido + fin)

            archivo.close()
            self.lblStatus.config(
                text="Guardado de archivo exitoso", bg="lightgreen")
        except:
            self.lblStatus.config(
                text="Guardado de archivo abortado.", bg="#FED8B1")

    def detachChanges(self):
        self.loadWorkspace()
        if (self.filesDirectory == ""):
            self.loadWorkspaceActions()
        else:
            self.loadWorkspaceActions()
            self.loadDirectoryActions()

    def printPoints(self):
        try:
            self.turtleScreen.tracer(False)
            self.lblStatus.config(
                text="Impresión de puntos en proceso", bg="lightblue")
            for i in self.ptsCoordinates:
                nuevopunto = turtle.RawTurtle(self.turtleScreen)
                nuevopunto.shape("circle")
                nuevopunto.color("green")
                nuevopunto.penup()
                nuevopunto.setx(i[0])
                nuevopunto.sety(480 - i[1])
                nuevopunto.turtlesize(0.15, 0.15, 0.15)
                nuevopunto.onclick(self.setActiveTurtle)
                self.turtles.append(nuevopunto)
            self.lblStatus.config(
                text="Impresión de puntos exitosa", bg="lightgreen")
            self.turtleScreen.tracer(True)
            self.forma_avanzar()
        except:
            raise Exception("Impresión de puntos abortada.")

    def setActiveTurtle(self, x, y):
        try:
            self.lblStatus.config(
                text="Proceso de selección de punto iniciado.", bg="lightblue")
            for index in range(len(self.turtles)):
                if (self.turtles[index].xcor()-5 <= x <= self.turtles[index].xcor()+5 and self.turtles[index].ycor()-5 <= y <= self.turtles[index].ycor()+5):
                    self.activeTurtleIndex = index

            self.turtleScreen.tracer(False)
            for turtle in self.turtles:
                turtle.color("green")
                turtle.turtlesize(0.15, 0.15, 0.15)
            self.turtleScreen.tracer(True)

            self.turtles[self.activeTurtleIndex].color("red")
            self.turtles[self.activeTurtleIndex].turtlesize(0.15, 0.15, 0.15)
            self.lblStatus.config(text="Punto " + str(self.activeTurtleIndex + 1) + " - (" + str(
                self.turtles[self.activeTurtleIndex].xcor()) + ", " + str(self.turtles[self.activeTurtleIndex].ycor()) + ")", bg="lightblue")
        except:
            self.lblStatus.config(
                text="Selección de punto abortado.", bg="#FED8B1")

    def loadWorkspace(self):
        try:
            self.lblStatus.config(
                text="Carga del espacio de trabajo en proceso", bg="lightblue")
            self.turtleScreen.clear()
            self.initConstants()
            self.loadPtsFile()
            self.updateTitle()
            self.loadImageBackground()
            self.printPoints()
            self.loadActions()
            self.lblStatus.config(
                text="Carga del espacio de trabajo exitosa, a la espera de interacción", bg="lightgreen")
        except Exception as e:
            raise Exception(str(e))


if (__name__ == "__main__"):
    app = App()
    app.screen.mainloop()
