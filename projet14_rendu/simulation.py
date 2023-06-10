import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider
from matplotlib import animation
import time
from numba import njit
from tqdm import tqdm
from Fenetre_parametre import App
from numpy import pi
import matplotlib.cm as cm
import matplotlib.colors as colors
from numba import jit

"""
TO DO LIST:
- LE ROULEMENT
- LE TABLEAU POUR LES VECTEUR NORMAUX ETC...
"""

#-------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------AFFICHAGE-----------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------#

 

def trajectoire(POSITION, nb_grains, Agauche, Cgauche, Adroite, Cdroite, paroiGauche, paroiDroite, debut_du_trou, hauteur_bac, largeur_bac_gauche, limite_gauche, limite_droite):
    """
    Affiche la trajectoire des grains dans un graphe matplotlib.

    Paramètres
    ==========
    Retour
    ======
    rien
    """
    print("Affichage de la trajectoire...")

    fig1, ax1 = plt.subplots()
    # dessin du silo dans le tableau graphique matplot
    # on trouve le x du debut du trou pour les deux parois:
    x_debut_du_trou_gauche = (debut_du_trou - Cgauche)/Agauche
    x_debut_du_trou_droite = (debut_du_trou - Cdroite)/Adroite

    # Parois et bac:
    X1 = np.linspace(limite_gauche, x_debut_du_trou_gauche, 100)
    X2 = np.linspace(x_debut_du_trou_droite, limite_droite, 100)
    X3 = np.linspace(-largeur_bac_gauche, largeur_bac_gauche, 100)
    Y3 = np.zeros(100) + hauteur_bac
    ax1.plot(X1, paroiGauche(X1), color='#EEEEEE')
    ax1.plot(X2, paroiDroite(X2), color='#EEEEEE')
    ax1.plot(X3, Y3, color='#EEEEEE')
    

    for grain in range(nb_grains):
        ax1.plot(POSITION[:, grain, 0], POSITION[:, grain, 1])

    fig1.patch.set_facecolor('#222831') # On définit la couleur de fond de la figure
    plt.xlim([limite_gauche, limite_droite])
    plt.ylim([limite_bas, limite_haut])

    ax1.set_aspect('equal')
    ax1.set_facecolor('#222831') # On définit la couleur de fond de la figure
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.xaxis.label.set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.xaxis.label.set_color('#EEEEEE')
    ax1.grid(alpha=0.1)

    plt.legend()
    plt.show()



def grain_anime(POSITION, VITESSE, nb_grains, RAYON, Agauche, Cgauche, Adroite, Cdroite, paroiGauche, paroiDroite, debut_du_trou, hauteur_bac, largeur_bac_gauche, limite_gauche, limite_droite, nb_temps, pas_de_temps):
    """
    Fait une animation de la chute des grains dans le silo.

    Paramètres
    ==========
    POSITION : np.array, tableau des positions
    hauteur_silo : float, hauteur du silo
    largeur_silo : float, largeur du silo
    nb_grains : int, nombre de grains
    rayon : float, rayon des grains

    Retour
    ======
    rien    
    """
    print("Animation en cours...")
    # fenetre pour le curseur d'accelerateur
    slider_fig, slider_ax = plt.subplots(figsize=(6, 1))
    # Positionnement des axes de la fenêtre du curseur
    slider_ax.set_position([0.1, 0.45, 0.82, 0.1])
    # Valeur initiale de l'accélérateur
    accelerateur = 100
    # Fonction de mise à jour appelée lorsque la valeur du curseur change
    def update_accelerateur(val):
        nonlocal accelerateur
        nonlocal ani

        accelerateur = val
        # on empeche l'accelerateur d'etre nul
        if accelerateur == 0:
            accelerateur = 1
        # On stoppe l'animation en cours et on la relance avec la nouvelle valeur de l'accelerateur
        ani.event_source.stop()
        ani = animation.FuncAnimation(fig, animate, frames=int(POSITION.shape[0]/accelerateur), interval=1, blit=True)

    # Création du curseur
    accelerateur_slider = Slider(slider_ax, 'Vitesse', 0, 500, valinit=accelerateur, valstep=10)
    accelerateur_slider.on_changed(update_accelerateur)

    # fenetre de l'animation
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    
    # dessin du silo dans le tableau graphique matplot
    # on trouve le x du debut du trou pour les deux parois:
    x_debut_du_trou_gauche = (debut_du_trou - Cgauche)/Agauche
    x_debut_du_trou_droite = (debut_du_trou - Cdroite)/Adroite
    X1 = np.linspace(limite_gauche, x_debut_du_trou_gauche, 100)
    X2 = np.linspace(x_debut_du_trou_droite, limite_droite, 100)
    plt.plot(X1, paroiGauche(X1), color='#EEEEEE')
    plt.plot(X2, paroiDroite(X2), color='#EEEEEE')
    
    # dessin du bac de reception
    X3 = np.linspace(-largeur_bac_gauche, largeur_bac_gauche, 100)
    Y3 = np.zeros(100) + hauteur_bac
    plt.plot(X3, Y3, color='#EEEEEE')

    # dessin des grains dans le tableau graphique matplot
    couleurs = ['#EEEEEE', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown']
    grains = []
    for grain in range(nb_grains):
        grains.append(ax.add_patch(patches.Circle((POSITION[0, grain, 0], POSITION[0, grain, 1]), radius=RAYON[grain], fill=True, color=couleurs[grain%len(couleurs)])))
    
    time_text = ax.text(0.05, 0.99, '', transform=ax.transAxes, verticalalignment='top', fontsize=12, color='#EEEEEE')
    debit_text = ax.text(0.05, 0.05, "", transform=ax.transAxes, verticalalignment="bottom", fontsize=12, color='#EEEEEE')   

    def animate(frame):
    
        time_text.set_text(f"Indice temps: {frame*accelerateur}/{nb_temps}, temps(s): {frame*accelerateur*pas_de_temps:.2f}/{nb_temps*pas_de_temps:.2f}")

        for grain in range(nb_grains):
            vitesse = VITESSE[
                frame * accelerateur, grain
            ]  # Obtention de la vitesse du grain à l'étape temporelle
            couleur = plt.cm.jet(
                abs(vitesse)
            )  # Calcul de la couleur en fonction de la vitesse
            grains[grain].set_color(couleur[1])  # Mise à jour de la couleur du grain
            grains[grain].center = (
                POSITION[frame * accelerateur, grain, 0],
                POSITION[frame * accelerateur, grain, 1],
            )  # Mise à jour de la position du grain
        return grains + [time_text] + [debit_text] 

    
    ani = animation.FuncAnimation(fig, animate, frames=int(POSITION.shape[0]/accelerateur), interval=1, blit=True)
    # Normalisation des valeurs de vitesse
    norm = colors.Normalize(vmin=np.min(abs(VITESSE)), vmax=np.max(abs(VITESSE)))
    # Création de l'échelle de couleur
    cmap = cm.ScalarMappable(norm=norm, cmap='jet')
    cb = plt.colorbar(cmap)
    cb.set_label('Vitesse(m/s)', color='#EEEEEE')
    plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color="#EEEEEE")
    cb.ax.yaxis.set_tick_params(color='#EEEEEE')
    fig.patch.set_facecolor('#222831')                          # On définit la couleur de fond de la figure
    ax.set_facecolor('grey')                          # On définit la couleur de fond de la figure
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('#EEEEEE')
    ax.grid(alpha=0.1)
    plt.xlim([limite_gauche, limite_droite])
    plt.ylim([limite_bas, limite_haut])
    slider_fig.show()
    plt.show()


def debit(MASSE_PASSEE, nb_temps, pas_de_temps):
    print("Affichage du debit massique...")
    
    #On calcule le débit:
    DEBIT = np.zeros(nb_temps)
    for i in range(nb_temps):
        if i == 0 :
            DEBIT[0] = (-3*MASSE_PASSEE[0] + 4*MASSE_PASSEE[1] -MASSE_PASSEE[2])/(2*pas_de_temps)
        elif i == nb_temps-1:
            DEBIT[nb_temps-1] = (3*MASSE_PASSEE[nb_temps-1]-4*MASSE_PASSEE[nb_temps-2] + MASSE_PASSEE[nb_temps-3])/(2*pas_de_temps)
        else:
            DEBIT[i] = (MASSE_PASSEE[i+1] - MASSE_PASSEE[i-1])/(2*pas_de_temps)
 
 
    TIME = np.array([i for i in range(nb_temps)])
    
    # Intervalle mobile pour affiné les données
    IntervalleMobile = nb_temps//10000 #intervalle mobile
    
    DebitMobile = np.zeros(nb_temps+1-IntervalleMobile+1)
    MasseMobile = np.zeros(nb_temps+1-IntervalleMobile+1)
    TempsMobile = np.zeros(nb_temps+1-IntervalleMobile+1)
    for i in range (nb_temps+1-IntervalleMobile+1):
        #Masse passée
        MasseMobile[i] = np.mean(MASSE_PASSEE[i:i+IntervalleMobile])
        
        #Débit massique
        DebitMobile[i] = np.mean(DEBIT[i:i+IntervalleMobile])
        
        #Nouveau temps:
        TempsMobile[i] = TIME[i]

    fig1, ax1 = plt.subplots()   
    ax1.plot(TempsMobile, MasseMobile, color='blue', lw=1, label="masse passée au cours du temps(affiné)")
    ax1.plot(TempsMobile, DebitMobile, color='red', lw=1, label="débit massique instantané(affiné)")
    ax1.set_xlabel("Indice du temps.")
    ax1.set_ylabel("Masse passée en kg/Débit massique instantané kg.s-1.")
    ax1.set_title("Masse passé au cours du temps et débit massique instantané.")
    ax1.grid(alpha=0.1)
    
    
    start = 100  # index de début de l'intervalle
    end = int(len(TempsMobile)*1/2)  # index de fin de l'intervalle

    # réaliser une régression linéaire sur l'intervalle spécifié
    coeffs = np.polyfit(TempsMobile[start:end], DebitMobile[start:end], 1)  # 1 pour une régression linéaire
    slope, intercept = coeffs

    # créer une fonction pour la ligne de régression
    line = lambda x: slope * x + intercept

    # tracer les données
    ax1.plot(TempsMobile, line(TempsMobile), color='#FFCF1B', label=f'Ligne de régression: y={slope:.4f}x+{intercept:.4f}')

    
    plt.legend()
    plt.show()
    
    fig2, ax2 = plt.subplots()
    ax2.plot(TIME, DEBIT, color='black', lw=1, label="débit massique instantané(brut)")
    ax2.set_xlabel("Indice du temps.")
    ax2.set_ylabel("Débit massique instantané kg.s-1.")
    ax2.set_title("Débit massique instantané.")
    ax2.grid(alpha=0.1)
    plt.legend()
    plt.show()
    
    fig3, ax3 = plt.subplots()
    ax3.plot(TIME, MASSE_PASSEE, color='black', lw=1, label="masse passée au cours du temps(brut)")
    ax3.set_xlabel("Indice du temps.")
    ax3.set_ylabel("Masse passée en kg.")
    ax3.set_title("Masse passé au cours du temps.")
    ax3.grid(alpha=0.1)
    plt.legend()
    plt.show()






    #-------------------------------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------FONCTIONS-----------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------------------------------------------------#




@njit
def application_efforts_distance(masse):
    """
    Application des efforts à distance (par exemple la pesanteur).

    Paramètres
    ==========
    masse : float, masse du grain

    Retour
    ======
    forces : np.array, forces appliquée au grain
    """
    return np.array([0, -masse*9.81])

@njit
def allongement_normal_grain_grain(position_i, position_j, rayon_i, rayon_j):
    """
    Calcul de l'allongement normal entre deux grains i et j à partir de l'équation

    Paramètres
    ==========
    position_i : np.array, position du grain i
    position_j : np.array, position du grain j

    Retour
    ======
    allongement_normal : float, allongement normal entre les grains i et j
    """

    return np.sqrt((position_i[0] - position_j[0])**2 + (position_i[1] - position_j[1])**2) - (rayon_i + rayon_j)


# Distance à la paroi, droite d'équation: A*x + B*y + C = 0. Ici B=1, A=-Agauche/droite et C=-Cgauche/droite.
# La distance orthogonale est alors donné par la relation : d = abs(A*x + B*y + C) / sqrt(A**2 + B**2)
@njit
def allongement_normal_grain_paroi(position, rayon, A, C):
    """
    """

    distance_a_la_gauche = abs(-A * position[0] + 1*position[1] - C) / np.sqrt(A**2 + 1)
    penetration = distance_a_la_gauche - rayon

    return penetration


@njit
def allongement_tangentiel_grain_paroi(vitesse_i, vecteur_tangent_paroi, pas_de_temps, allongement_tangentiel):
    """
    """

    produit_scalaire = np.dot(vitesse_i , vecteur_tangent_paroi)

    return allongement_tangentiel + produit_scalaire*pas_de_temps


@njit
def allongement_tangentiel_grain_grain(position_i, position_j, vitesse_i, vitesse_j, pas_de_temps, allongement_tangentiel):
    """
    Calcul de l'allongement tangentiel entre deux grains i et j à partir de l'équation

    Paramètres
    ==========
    POSITION : np.array, position des grains
    VITESSE : np.array, vitesse des grains
    i : int, indice du grain i
    j : int, indice du grain j
    indice_temps : int, indice du temps
    
    Retour
    ======
    allongement_tangentiel : float, allongement tangentiel entre les grains i et j
    """
    vecteur_normal = (position_i - position_j)/(np.linalg.norm(position_i - position_j))
    vecteur_tangent = np.array([-vecteur_normal[1], vecteur_normal[0]])
    produit_scalaire = np.dot(vitesse_i - vitesse_j, vecteur_tangent)

    return allongement_tangentiel + produit_scalaire*pas_de_temps

@njit
def derivee_allongement_grain_grain(vitesse_i, vitesse_j, vecteur):
    """
    Calcul de la dérivée de l'allongement/distance normal à partir de l'équation
    Paramètres
    ==========

    Retour
    ======
    """
    vitesse_relative = vitesse_i - vitesse_j
    derivee_allongement = np.dot(vitesse_relative,vecteur)
        
    return derivee_allongement

@njit
def derivee_allongement_grain_paroi(vitesse_i, vecteur_paroi):
    """
    """
    return np.dot(vitesse_i, vecteur_paroi)


def maj_grille(GRILLE, POSITION, indice_temps, limite_gauche, limite_bas, mise_a_jour, c):
    """
    Fonction d'actulaisation de la grille.

    Paramètres
    ==========
    GRILLE: np.bool, grille de l'espace.
    POSITION: np.float, tableau de position des grains.
    indice_temps: int, indice du temps de la boucle temporelle.
    limite_gauche: float, limite gauche de l'espace.
    limite_bas: float, limite bas de l'espace.
    mise_a_jour: np.bool, liste dont les indices sont ceux des grains et la valeur booléenne indiquant s'il doit être mis jour.
    c: float, pas d'espace.
    

    Retour
    ======
    GRILLE: np.bool, grille de l'espace.
    """
    # Grille
    for grain, maj in enumerate(mise_a_jour):
        if maj:
            # On associe à chaque case de la grille les grains qui sont dans cette case
            # Probleme car pos_case peut etre negatif pour ca on déplace le repere
                pos_case = (int((POSITION[indice_temps, grain, 0] + limite_gauche)/c), int((POSITION[indice_temps,grain,1]+ limite_bas)/c))
                GRILLE[pos_case[0], pos_case[1], grain] = True

    return GRILLE

@njit
def actualisation_1(POSITION, VITESSE_DEMI_PAS, VITESSE, ACCELERATION, indice_temps, pas_de_temps):
    """
    Fonction qui actualise la grille, la position et la vitesse des grains à l'instant k

    Paramètres
    ==========
    POSITION: np.float, tableau de position des grains.
    VITESSE_DEMI_PAS: np.float, tableau de vitesse à demi pas de temps des grains.
    VITESSE: np.float, tableau de vitesse des grains.
    ACCELERATION: np.float, tableau de l'accélération des grains.
    indice_temps: int, indice du temps de la boucle temporelle.
    pas_de_temps: float, pas de temps de la simulation.


    Retour
    ======
    POSITION: np.float, tableau de position des grains.
    VITESSE: np.float, tableau de vitesse des grains.
    """
    # Actualisation position et vitesse
    POSITION[indice_temps] = POSITION[indice_temps-1] + VITESSE_DEMI_PAS[indice_temps-1]*pas_de_temps
    VITESSE[indice_temps] = VITESSE_DEMI_PAS[indice_temps-1] + ACCELERATION[indice_temps-1]*pas_de_temps/2

    return POSITION, VITESSE

@njit
def voisinage(mise_a_jour, grain, x, y, GRILLE):
    """
    Détermine la liste de voisinage du grain i

    Paramètres
    ==========
    grain : int, indice du grain
    x : int, indice de la ligne du grain
    y : int, indice de la colonne du grain
    GRILLE : np.array, grille des grains

    Retour
    ======
    voisinage : liste, tableau des indices des grains en contact avec le grain i
    """
    voisinage = []

    for j in range(-1, 2):
        for k in range(-1, 2):
            for i, bit in enumerate(GRILLE[x+j,y+k]):
                if bit and mise_a_jour[i] and i != grain:
                    voisinage.append(i)


    return voisinage

@njit
def maj_contact(limite_bas, CONTACT, coefficient_frottement, raideur_normale, raideur_tangentielle, GRILLE, mise_a_jour, indice_temps, nb_grains, POSITION, RAYON, Agauche, Adroite, Cgauche, Cdroite, limite_gauche, ALLONGEMENT, VITESSE, debut_du_trou, pas_de_temps, vecteur_tangent_paroi_droite, vecteur_tangent_paroi_gauche, hauteur_bac):
    """
    Met à jour la liste des contacts

    Paramètres
    ==========

    Retour
    ======
    """

    nouveau_contact = np.zeros((nb_grains, nb_grains+3, 2)) # premiere valeur: indice du contact oui ou non, deuxieme: glissement ou non
    nouveau_allongement = np.zeros((nb_grains, nb_grains+3, 2), dtype=np.float64) # premiere valeur: normale, deuxieme: tangentielle
    vecteur_tangent_bac = np.array([1.0, 0.0])
    for i, maj in enumerate(mise_a_jour):
        if maj:
            pos_i = POSITION[indice_temps, i]
            vitesse_i = VITESSE[indice_temps, i]
            rayon_i = RAYON[i]

            # Contact avec les parois ?
            if pos_i[1] >= debut_du_trou:
                penetration_gauche = allongement_normal_grain_paroi(pos_i, rayon_i, Agauche, Cgauche)

                if penetration_gauche < 0:
                    nouveau_contact[i, nb_grains, 0] = True
                    nouveau_allongement[i, nb_grains, 0] = penetration_gauche
                    Fn = -penetration_gauche * raideur_normale
                    # On vérifie le type de glissement contact ou pas:
                    #Effort tangentiel:
                    allongement_tangentiel = ALLONGEMENT[i, nb_grains, 1]
                    allongement_tangentiel = allongement_tangentiel_grain_paroi(vitesse_i, vecteur_tangent_paroi_gauche, pas_de_temps, allongement_tangentiel)
                    Ft = -raideur_tangentielle * allongement_tangentiel
                    # Non Glissement
                    if abs(Ft) <= coefficient_frottement * abs(Fn):
                        nouveau_allongement[i, nb_grains, 1] = allongement_tangentiel
                    # Oui Glissement
                    else:
                        nouveau_contact[i, nb_grains, 1] = True
                        nouveau_allongement[i, nb_grains, 1] = np.sign(allongement_tangentiel)*coefficient_frottement * abs(Fn) / raideur_tangentielle # En mode glissement


                else:
                    penetration_droite = allongement_normal_grain_paroi(pos_i, rayon_i, Adroite, Cdroite)
                    if penetration_droite < 0:
                        nouveau_contact[i, nb_grains+1, 0] = True
                        nouveau_allongement[i, nb_grains+1, 0] = penetration_droite
                        Fn = -penetration_droite * raideur_normale
                        # On vérifie le type de glissement contact ou pas:
                        #Effort tangentiel:
                        allongement_tangentiel = ALLONGEMENT[i, nb_grains+1, 1]
                        allongement_tangentiel = allongement_tangentiel_grain_paroi(vitesse_i, vecteur_tangent_paroi_droite, pas_de_temps, allongement_tangentiel)
                        Ft = -raideur_tangentielle * allongement_tangentiel
                        # Non Glissement
                        if abs(Ft) <= coefficient_frottement * abs(Fn):
                            nouveau_allongement[i, nb_grains+1, 1] = allongement_tangentiel
                        # Oui Glissement
                        else:
                            nouveau_contact[i, nb_grains+1, 1] = True
                            nouveau_allongement[i, nb_grains+1, 1] = np.sign(allongement_tangentiel)*coefficient_frottement * abs(Fn) / raideur_tangentielle # En mode glissement

            # Contact avec le bac ?
            else:
                distance_bac = pos_i[1] - hauteur_bac
                penetration_bac = distance_bac - rayon_i
                if penetration_bac < 0:
                    nouveau_contact[i, nb_grains+2, 0] = True
                    nouveau_allongement[i, nb_grains+2, 0] = penetration_bac
                    Fn = -penetration_bac * raideur_normale
                    # On vérifie le type de glissement contact ou pas:
                    #Effort tangentiel:
                    allongement_tangentiel = ALLONGEMENT[i, nb_grains+2, 1]
                    allongement_tangentiel = allongement_tangentiel_grain_paroi(vitesse_i, vecteur_tangent_bac, pas_de_temps, allongement_tangentiel)
                    Ft = -raideur_tangentielle * allongement_tangentiel
                    # Non Glissement
                    if abs(Ft) <= coefficient_frottement * abs(Fn):
                        nouveau_allongement[i, nb_grains+2, 1] = allongement_tangentiel
                    # Oui Glissement
                    else:
                        nouveau_contact[i, nb_grains+2, 1] = True
                        nouveau_allongement[i, nb_grains+2, 1] = np.sign(allongement_tangentiel)*coefficient_frottement * abs(Fn) / raideur_tangentielle # En mode glissement 



            # Contact avec un autre grain ?
            pos_case = (int((pos_i[0] + limite_gauche)/c), int((pos_i[1] + limite_bas)/c))
            voisins = voisinage(mise_a_jour, i, pos_case[0], pos_case[1], GRILLE)
            for j in voisins:
                if i != j: # pas besoin de check le mise a jour car 'voisins' ne peut pas contenir les grains pas à jour
                    pos_j = POSITION[indice_temps, j]
                    vitesse_j = VITESSE[indice_temps, j]
                    rayon_j = RAYON[j]

                    allongement_normal = allongement_normal_grain_grain(pos_i, pos_j, rayon_i, rayon_j)
                    if allongement_normal < 0:
                        nouveau_contact[i, j, 0] = True
                        nouveau_allongement[i, j, 0] = allongement_normal
                        Fn = -allongement_normal * raideur_normale
                        # On vérifie le type de glissement contact ou pas:
                        #Effort tangentiel:
                        allongement_tangentiel = ALLONGEMENT[i, j, 1]
                        allongement_tangentiel = allongement_tangentiel_grain_grain(pos_i, pos_j, vitesse_i, vitesse_j, pas_de_temps, allongement_tangentiel)
                        Ft = -raideur_tangentielle * allongement_tangentiel
                        norme_tangent = abs(Ft)
                        # Non Glissement
                        if norme_tangent <= coefficient_frottement * abs(Fn):
                            nouveau_allongement[i, j, 1] = allongement_tangentiel
                        # Oui Glissement
                        else:
                            nouveau_contact[i, j, 1] = True
                            nouveau_allongement[i, j, 1] = np.sign(allongement_tangentiel)*coefficient_frottement * abs(Fn) / raideur_tangentielle # En mode glissement
    
    return nouveau_contact, nouveau_allongement


@njit
def resultante_et_actualisation_2(activatebox, coefficient_frottement, mise_a_jour, indice_temps, AMORTISSEMENT, POSITION, VITESSE, MASSE, RAYON, CONTACT, ALLONGEMENT, ACCELERATION, VITESSE_DEMI_PAS, nb_grains, raideur_normale, raideur_tangentielle, coefficient_trainee, vecteur_orthogonal_paroi_gauche, vecteur_orthogonal_paroi_droite, vecteur_tangent_paroi_gauche, vecteur_tangent_paroi_droite):
    """
    Fonction qui calcule la force résultante et actualise l'accélération à l'instant k et la vitesse des grains à l'instant k+1/2

    Paramètres
    ==========


    Retour
    ======
    """

    for grain1, maj in enumerate(mise_a_jour):

        if maj:
            #Variables utiles:
            position_grain1 = POSITION[indice_temps, grain1]
            vitesse_grain1 = VITESSE[indice_temps, grain1]
            masse_grain1 = MASSE[grain1]
            rayon_grain1 = RAYON[grain1]
            tableau_contact_grain1 = CONTACT[grain1] # de la forme (nbgrains+2, 1)
            amortissement_grain1 = AMORTISSEMENT[grain1]


            #Initialisation force résultante:
            force_resultante = application_efforts_distance(masse_grain1) #Force à distance = gravité
            for obstacle, contact in enumerate(tableau_contact_grain1):
                en_contact = contact[0] # car c'est 2D, donc on prend juste le boolen du contact ici
                glissement = contact[1]

                # S'il y a contact:
                if en_contact:
                    
                    # Rencontre avec une paroi du silo ?
                    # Paroi gauche
                    if obstacle == nb_grains:
                        penetration_gauche = ALLONGEMENT[grain1, nb_grains, 0]
                        allongement_tangentiel = ALLONGEMENT[grain1, nb_grains, 1]
                        
                        # Effort normal:
                        Fn = -raideur_normale * penetration_gauche
                        force_resultante += Fn * vecteur_orthogonal_paroi_gauche
                        #Amortissement:
                        derivee_amortissement = derivee_allongement_grain_paroi(vitesse_grain1, vecteur_orthogonal_paroi_gauche)
                        force_resultante += -amortissement_grain1 * derivee_amortissement * vecteur_orthogonal_paroi_gauche
                        
                        #Effort tangentiel:
                        Ft = -raideur_tangentielle * allongement_tangentiel
                        #Amortissement:
                        #derivee_amortissement = derivee_allongement_grain_paroi(vitesse_grain1, vecteur_tangent_paroi_gauche)
                        #force_resultante += -amortissement_grain1 * derivee_amortissement * vecteur_tangent_paroi_gauche
                        # Glissement
                        if glissement:
                            force_tangentielle = np.sign(Ft) * coefficient_frottement * abs(Fn) * vecteur_tangent_paroi_gauche
                            force_resultante += force_tangentielle
                        else:
                            force_tangentielle = Ft * vecteur_tangent_paroi_gauche
                            force_resultante += force_tangentielle


                    # Paroi droite
                    elif obstacle == nb_grains+1:
                        penetration_droite = ALLONGEMENT[grain1, nb_grains+1, 0]
                        allongement_tangentiel = ALLONGEMENT[grain1, nb_grains+1, 1]
                        
                        # Effort normal:
                        Fn = -raideur_normale * penetration_droite
                        force_resultante += Fn* vecteur_orthogonal_paroi_droite
                        # Amortissement:
                        derivee_amortissement = derivee_allongement_grain_paroi(vitesse_grain1, vecteur_orthogonal_paroi_droite)
                        force_resultante += -amortissement_grain1 * derivee_amortissement * vecteur_orthogonal_paroi_droite
                        
                        # Effort tangentiel:
                        Ft = -raideur_tangentielle * allongement_tangentiel
                        #Amortissement:
                        #derivee_amortissement = derivee_allongement_grain_paroi(vitesse_grain1, vecteur_tangent_paroi_droite)
                        #force_resultante += -amortissement_grain1 * derivee_amortissement * vecteur_tangent_paroi_droite
                        # Glissement
                        if glissement:
                            force_tangentielle = np.sign(Ft) * coefficient_frottement * abs(Fn) * vecteur_tangent_paroi_droite
                            force_resultante += force_tangentielle
                        else:
                            force_tangentielle = Ft * vecteur_tangent_paroi_droite
                            force_resultante += force_tangentielle
                    
                    # Bac
                    elif obstacle == nb_grains+2:
                        vecteur_normal_bac = np.array([0.0, 1.0])
                        vecteur_tangent_bac = np.array([1.0, 0.0])
                        # Si la physique du bac est activé:
                        if activatebox:
                            penetration_bac = ALLONGEMENT[grain1, nb_grains+2, 0]
                            allongement_tangentiel = ALLONGEMENT[grain1, nb_grains+2, 1]
                            
                            # Effort normal:
                            Fn = -raideur_normale * penetration_bac
                            force_resultante += Fn * vecteur_normal_bac
                            # Amortissement:
                            derivee_amortissement = derivee_allongement_grain_paroi(vitesse_grain1, vecteur_normal_bac)
                            force_resultante += -amortissement_grain1 * derivee_amortissement * vecteur_normal_bac
                            
                            # Effort tangentiel:
                            Ft = -raideur_tangentielle * allongement_tangentiel
                             #Amortissement:
                            #derivee_amortissement = derivee_allongement_grain_paroi(vitesse_grain1, vecteur_tangent_bac)
                            #force_resultante += -amortissement_grain1 * derivee_amortissement * vecteur_tangent_bac
                            # Glissement
                            if glissement:
                                force_tangentielle = np.sign(Ft) * coefficient_frottement * abs(Fn) * vecteur_tangent_bac
                                force_resultante += force_tangentielle
                            else:
                                force_tangentielle = Ft * vecteur_tangent_bac
                                force_resultante += force_tangentielle
                        
                            if vitesse_grain1[0] < 0 and position_grain1[0]<-0.4:
                                print(allongement_tangentiel)

                        # Si la physique du bac n'est pas activé:        
                        else:
                            VITESSE[indice_temps, grain1] = np.array([0.0,0.0])
                            ACCELERATION[indice_temps, grain1] = np.array([0.0,0.0])
                            VITESSE_DEMI_PAS[indice_temps, grain1] = np.array([0.0,0.0])
                            mise_a_jour[grain1] = False
                    
                    # Rencontre avec un autre grain ?
                    else:
                        # Variables utiles:
                        grain2 = obstacle
                        position_grain2 = POSITION[indice_temps, grain2]
                        vitesse_grain2 = VITESSE[indice_temps, grain2]
                        allongement_normal = ALLONGEMENT[grain1, grain2, 0]
                        allongement_tangentiel = ALLONGEMENT[grain1, grain2, 1]
                        vecteur_normal_inter_grain = (position_grain1 - position_grain2)/(np.linalg.norm(position_grain1 - position_grain2))
                        vecteur_tangentiel_inter_grain = np.array([-vecteur_normal_inter_grain[1], vecteur_normal_inter_grain[0]])
                        
                        # Effort normal:
                        Fn = -raideur_normale * allongement_normal
                        force_resultante += Fn * vecteur_normal_inter_grain
                        # Amortissement:
                        derivee_amortissement = derivee_allongement_grain_grain(vitesse_grain1, vitesse_grain2, vecteur_normal_inter_grain)
                        force_resultante += - amortissement_grain1 * derivee_amortissement * vecteur_normal_inter_grain
                        
                        # Effort tangentiel:
                        Ft = -raideur_tangentielle * allongement_tangentiel
                        # Amortissement:
                        #derivee_amortissement = derivee_allongement_grain_grain(vitesse_grain1, vitesse_grain2, vecteur_tangentiel_inter_grain)
                        #force_resultante += - amortissement_grain1 * derivee_amortissement * vecteur_tangentiel_inter_grain
                        # Glissement
                        if glissement:
                            force_tangentielle = np.sign(Ft) * coefficient_frottement * Fn * vecteur_tangentiel_inter_grain
                            force_resultante += force_tangentielle
                        else:
                            force_tangentielle = Ft * vecteur_tangentiel_inter_grain
                            force_resultante += force_tangentielle
                    
                    # Air:
                    # Force de trainée:
                    norme_vitesse = np.linalg.norm(vitesse_grain1)
                    if norme_vitesse > 0:
                        frotemment_air = (1/2)*rho*(4*pi*rayon_grain1**2)*coefficient_trainee*norme_vitesse**2
                        vecteur_directeur_vitesse = vitesse_grain1/norme_vitesse
                        force_resultante += -frotemment_air*vecteur_directeur_vitesse
                        
            # Calcul de l'accélération du grain à partir de l'équation
            ACCELERATION[indice_temps, grain1] = force_resultante / masse_grain1
            # Calcul de la vitesse de demi-pas à k+1/2 à partir de l'équation
            VITESSE_DEMI_PAS[indice_temps, grain1] = VITESSE_DEMI_PAS[indice_temps-1, grain1] + ACCELERATION[indice_temps, grain1] * pas_de_temps

    return mise_a_jour, ACCELERATION, VITESSE_DEMI_PAS, CONTACT, VITESSE, VITESSE_DEMI_PAS

@njit
def actu_masse_passee(nb_grains, POSITION, indice_temps, debut_du_trou, MASSE):
    masse_actuelle_passee = 0
    for i in range(nb_grains):
        if POSITION[indice_temps][i][1] < debut_du_trou: 
            masse_actuelle_passee += MASSE[i]
    
    return masse_actuelle_passee


#-------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------DEFINITION----------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------#
"""
Pour un grain de blé circulaire, voici quelques valeurs typiques :

Diamètre moyen d'un grain de blé : 5 à 7 millimètres (0,005 à 0,007 mètres)
Masse volumique du blé : environ 780 à 820 kg/m³
Coefficient de traînée (Cd) pour un grain de blé : environ 0,47
"""

if __name__ == "__main__":


    app = App()
    app.racine.mainloop()
    plt.close('all')
#-----------------------------------------------------------------------------------------------------------------------------------------------
    # GRAIN
    nb_grains = app.nbGrains
    rayon = 5e-3 #m
    rho = 770 #kg/m3
    RAYON = np.random.uniform(low=rayon*0.8, high=rayon*1.2, size=nb_grains)
    MASSE = rho * 4/3 * pi * RAYON**3
    raideur_normale = rho #N/m
    raideur_tangentielle = 1/2*raideur_normale #N/m
    coefficient_trainee = 0.47
    AMORTISSEMENT = np.sqrt(raideur_normale*MASSE)*0.12
#-----------------------------------------------------------------------------------------------------------------------------------------------
    # TEMPS
    temps = 0
    indice_temps = 0
    pas_de_temps = np.sqrt(np.min(MASSE)/raideur_normale)*0.15#s
    duree_simulation = app.dureeSimulation #s
    nb_temps = int(duree_simulation/pas_de_temps)
#-----------------------------------------------------------------------------------------------------------------------------------------------
    # ESPACE
    limite_bas = app.limite_bas  #m
    limite_haut = app.limite_haut #m
    limite_gauche = app.limite_gauche #m
    limite_droite = app.limite_droite #m
    coefficient_frottement = 0.1
    # Définition de la grille
    c = 5*rayon #pas d'espace de la grille en m
    # On définit une grille pour discrétiser l'espace selon le pas d'espace c, a chaque case on met la liste des grains qui sont dans cette case
    nb_cases_x = int((limite_droite - limite_gauche)/c) + 2
    nb_cases_y = int((limite_haut - limite_bas)/c) + 2
    GRILLE = np.zeros(( nb_cases_x , nb_cases_y, nb_grains), dtype=bool) #on définit une grille vide #ancienne version : GRILLE = {(i,j):[] for i in range(int(limite_gauche/c)-1, int(limite_droite/c)+2) for j in range(int(limite_bas/c)-1, int(limite_haut/c)+2)}
#-----------------------------------------------------------------------------------------------------------------------------------------------
    # TABLEAUX DE DONNEES:
    POSITION = np.zeros((nb_temps, nb_grains, 2))   
    VITESSE = np.zeros((nb_temps, nb_grains, 2))
    VITESSE_DEMI_PAS = np.zeros((nb_temps, nb_grains, 2))
    ACCELERATION = np.zeros((nb_temps, nb_grains, 2))
    CONTACT = np.zeros((nb_grains, nb_grains+3, 2), dtype=bool)
    ALLONGEMENT = np.zeros((nb_grains, nb_grains+3, 2), dtype=np.float64)

    # VARIABLE POUR LE DEBIT
    MASSE_PASSEE = np.zeros(nb_temps, dtype=np.float64)

    mise_a_jour = np.array([True for i in range(nb_grains)], dtype=bool) + True  #liste qui permet de savoir si on doit mettre à jour le grain ou pas
#-----------------------------------------------------------------------------------------------------------------------------------------------
    # SILO:
    # Definition bac de réception
    hauteur_bac = app.hauteurBac #m
    largeur_bac_gauche = app.largeurBac/2 #m
    largeur_bac_droite = app.largeurBac/2 #m
    # On définit les droites des parois des silos comme des droites de la forme y = Ax + C afin de mettre sous la forme -Ax + y - C = 0
    CoeffDir = app.CoeffDir
    OrdOrigine = app.OrdOrigine
    debut_du_trou = app.debutTrou
    Agauche = CoeffDir
    Adroite = -CoeffDir
    Cgauche = OrdOrigine
    Cdroite = OrdOrigine
    activatebox = int(app.activateBoxPhysic.get())

    paroiGauche = lambda x : Agauche*x + Cgauche
    vecteur_directeur_paroi_gauche = np.array([1.0, Agauche])/ np.sqrt(1 + (Agauche)**2) #pointe vers le haut, normalisé
    vecteur_orthogonal_paroi_gauche = np.array([-Agauche, 1.0])/ np.sqrt(1 + (Agauche)**2) #pointe vers l'intérieur du silo, normalisé
    paroiDroite = lambda x : Adroite*x+Cdroite
    vecteur_directeur_paroi_droite = np.array([1.0, Adroite])/ np.sqrt(1 + (Agauche)**2) #pointe vers le haut, normalisé
    vecteur_orthogonal_paroi_droite = np.array([-Adroite, 1.0])/ np.sqrt(1 + (Agauche)**2) #pointe vers l'intérieur du silo, normalisé
    vecteur_tangent_paroi_gauche = np.array([-vecteur_orthogonal_paroi_gauche[1], vecteur_orthogonal_paroi_gauche[0]])
    vecteur_tangent_paroi_droite = np.array([-vecteur_orthogonal_paroi_droite[1], vecteur_orthogonal_paroi_droite[0]])
#-----------------------------------------------------------------------------------------------------------------------------------------------
    #Positionnement initiale des grains
    hauteur = app.hauteur #m
    gauche = (hauteur - Cgauche)/Agauche + rayon*1.3
    droite = (hauteur - Cdroite)/Adroite - rayon*1.3
    grain = 0 # compteur grain
    q = 0 # compteur colonne
    while grain < nb_grains:
        while True:
            x = gauche + (rayon*1.3*2)*q
            y = hauteur
            if x > droite or grain >= nb_grains:
                break
            else:
                POSITION[0, grain, 0] = x
                POSITION[0, grain, 1] = y
                grain += 1
                q += 1
        if grain < nb_grains:
            q = 0
            hauteur -= rayon*1.3*2
            gauche = (hauteur - Cgauche)/Agauche + rayon*1.3
            droite = (hauteur - Cdroite)/Adroite - rayon*1.3
            x = gauche + (rayon*1.3*2)*q
            y = hauteur
            POSITION[0, grain, 0] = x
            POSITION[0, grain, 1] = y
            grain += 1
            q += 1
        else:
            break

    
    # Affichage des infos implicites:
    print(f"nombre de grain: {nb_grains}")
    print(f"pas de temps: {pas_de_temps:.2E} s.")
    print(f"nombre de temps: {nb_temps}.")
    print(f"raideur normale: {raideur_normale:.2E} N/m.")
    print(f"masse moyenne des grains: {np.mean(MASSE):.2E} kg.")
    print(f"rayon moyen des grains: {np.mean(RAYON):.2E} m.")
    print(f"amoortissement moyen: {np.mean(AMORTISSEMENT):.2E} Ns/m.")
    print(f"durée de la simulation {duree_simulation} s")
    print(f"coefficient de frotemment:", coefficient_frottement)

#-----------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------SIMULATION-------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

    # Boucle principale
    print("Simulation en cours...")

    start_time = time.time()
    ancien_temps = temps
    for indice_temps in tqdm(range(1, nb_temps)):
        # Actualisation du temps
        temps += pas_de_temps

        # Actualisation de la position et de la vitesse
        POSITION, VITESSE = actualisation_1(POSITION, VITESSE_DEMI_PAS, VITESSE, ACCELERATION, indice_temps, pas_de_temps)   

        #On met à jour la grille:
        if indice_temps % 5 == 0:
            # Pour éviter les doublons dans la prochaine case de la grille on la réinitialise:
            GRILLE = np.zeros(( nb_cases_x , nb_cases_y, nb_grains), dtype=bool)
            GRILLE = maj_grille(GRILLE, POSITION, indice_temps, limite_gauche, limite_bas, mise_a_jour, c)
        
        # Mise à jour des deux tableaux CONTACT et ALLONGEMENT:
        CONTACT, ALLONGEMENT = maj_contact(limite_bas, CONTACT, coefficient_frottement, raideur_normale, raideur_tangentielle, GRILLE, mise_a_jour, indice_temps, nb_grains, POSITION, RAYON, Agauche, Adroite, Cgauche, Cdroite, limite_gauche, ALLONGEMENT, VITESSE, debut_du_trou, pas_de_temps, vecteur_tangent_paroi_droite, vecteur_tangent_paroi_gauche, hauteur_bac)
        
        # Calcul des efforts de contact pour mise à jour des vitesses à temps k+1/2 et accélérations à temps k
        mise_a_jour, ACCELERATION, VITESSE_DEMI_PAS, CONTACT, VITESSE, VITESSE_DEMI_PAS = resultante_et_actualisation_2(activatebox, coefficient_frottement, mise_a_jour, indice_temps, AMORTISSEMENT, POSITION, VITESSE, MASSE, RAYON, CONTACT, ALLONGEMENT, ACCELERATION, VITESSE_DEMI_PAS, nb_grains, raideur_normale, raideur_tangentielle, coefficient_trainee, vecteur_orthogonal_paroi_gauche, vecteur_orthogonal_paroi_droite, vecteur_tangent_paroi_gauche, vecteur_tangent_paroi_droite)
        
        # Mise à jour du tableau MASSE_PASSEE:
        MASSE_PASSEE[indice_temps] = actu_masse_passee(nb_grains, POSITION, indice_temps, debut_du_trou, MASSE)

    # Fin de la boucle principale
    print("Fin de la simulation")
    print("Temps de calcul: ", time.time() - start_time, "secondes")


    #Affichage:
    debit(MASSE_PASSEE, nb_temps, pas_de_temps)
    x_debut_du_trou_gauche = (debut_du_trou - Cgauche)/Agauche
    x_debut_du_trou_droite = (debut_du_trou - Cdroite)/Adroite
    D = x_debut_du_trou_droite - x_debut_du_trou_gauche
    print("Le diametre d'ouverture est de:", D, "m.")
    trajectoire(POSITION, nb_grains, Agauche, Cgauche, Adroite, Cdroite, paroiGauche, paroiDroite, debut_du_trou, hauteur_bac, largeur_bac_gauche, limite_gauche, limite_droite)
    grain_anime(POSITION, VITESSE, nb_grains, RAYON, Agauche, Cgauche, Adroite, Cdroite, paroiGauche, paroiDroite, debut_du_trou, hauteur_bac, largeur_bac_gauche, limite_gauche, limite_droite, nb_temps, pas_de_temps)
