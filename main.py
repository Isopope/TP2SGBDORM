from sqlalchemy import create_engine,Table,Column,Integer,String,Date,ForeignKey,Double,Time,insert
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3308/universite",echo=True)
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()

class Enseigner(Base):
    __tablename__='Enseigner'
    idProfesseur=Column(Integer,ForeignKey('Professeur.idProfesseur'), primary_key=True)
    idDepartement=Column(Integer,ForeignKey('Departement.idDepartement'), primary_key=True)

class Proposer(Base):
    __tablename__='Proposer'
    idDepartement=Column(Integer,ForeignKey('Departement.idDepartement'), primary_key=True)
    idCours=Column(Integer,ForeignKey('Cours.idCours'), primary_key=True)

class Sinscrire(Base):
    __tablename__='Sinscrire'
    idEtudiant=Column(Integer,ForeignKey('Etudiant.idEtudiant'), primary_key=True)
    idClasse=Column(Integer,ForeignKey('Classe.idClasse'), primary_key=True)
    note=Column(Double)

class Contrat(Base):
    __tablename__ = 'Contrat'
    Id_Contrat = Column(Integer, primary_key=True)
    typeContrat = Column(String(50))
    professeur=relationship('Professeur',back_populates='contrat')

class Batiment(Base):
    __tablename__ = 'Batiment'
    idBatiment = Column(Integer, primary_key=True)
    nomBatiment = Column(String(50))
    salles=relationship('Salle',back_populates='batiments')

class Professeur(Base):
    __tablename__ = 'Professeur'
    idProfesseur = Column(Integer, primary_key=True)
    nomProfesseur = Column(String(50))
    Id_Contrat = Column(Integer, ForeignKey('Contrat.Id_Contrat'))
    contrat=relationship('Contrat',back_populates='professeur')
    courss=relationship('Cours',back_populates='professeurs')
    departements=relationship('Departement',secondary='Enseigner',back_populates='professeurs')
    facultes=relationship('Faculte',back_populates='doyen_professor')
    departement_president=relationship('Departement',back_populates='president_professor')
    etudiant_conseiller=relationship('Etudiant',back_populates='professeur_conseiller')

class Cours(Base):
    __tablename__ = 'Cours'
    idCours = Column(Integer, primary_key=True)
    nomCours = Column(String(50))
    idProfesseur = Column(Integer, ForeignKey('Professeur.idProfesseur'))
    professeurs=relationship('Professeur',back_populates='courss')
    departements=relationship('Departement',secondary='Proposer',back_populates='courss')
    classe_cours=relationship('Classe',back_populates='cours_classe')

class Salle(Base):
    __tablename__ = 'Salle'
    idSalle = Column(Integer, primary_key=True)
    codeSalle = Column(String(50))
    idBatiment = Column(Integer, ForeignKey('Batiment.idBatiment'))
    batiments=relationship('Batiment',back_populates='salles')
    classe_deroule=relationship('Classe',back_populates='salle_deroule')

class Faculte(Base):
    __tablename__ = 'Faculte'
    idFaculte = Column(Integer, primary_key=True)
    nomFaculte = Column(String(50))
    idProfesseur = Column(Integer, ForeignKey('Professeur.idProfesseur'))
    doyen_professor=relationship('Professeur',back_populates='facultes')
    departement_comprend=relationship('Departement',back_populates='faculte_comprend')

class Classe(Base):
    __tablename__ = 'Classe'
    idClasse = Column(Integer, primary_key=True)
    nomClasse = Column(String(50))
    nombrePlace = Column(Integer)
    dateClasse = Column(Date)
    heureDebut = Column(Time)
    heureFin = Column(Time)
    idSalle = Column(Integer, ForeignKey('Salle.idSalle'))
    idCours = Column(Integer, ForeignKey('Cours.idCours'))
    salle_deroule=relationship('Salle',back_populates='classe_deroule')
    cours_classe=relationship('Cours',back_populates='classe_cours')
    etudiants=relationship('Etudiant',secondary='Sinscrire',back_populates='classes')

class Departement(Base):
    __tablename__ = 'Departement'
    idDepartement = Column(Integer, primary_key=True)
    nomDepartement = Column(String(50))
    idFaculte = Column(Integer, ForeignKey('Faculte.idFaculte'))
    idProfesseur = Column(Integer, ForeignKey('Professeur.idProfesseur'))
    faculte_comprend=relationship('Faculte',back_populates='departement_comprend')
    professeurs=relationship('Professeur',secondary='Enseigner',back_populates='departements')
    president_professor=relationship('Professeur',back_populates='departement_president')
    courss=relationship('Cours',secondary='Proposer',back_populates='departements')
    specialite_departement=relationship('Specialite',back_populates='departement_specialite')

class Specialite(Base):
    __tablename__ = 'Specialite'
    idSpecialite = Column(Integer, primary_key=True)
    nomSpecialite = Column(String(50))
    idDepartement = Column(Integer, ForeignKey('Departement.idDepartement'))
    departement_specialite=relationship('Departement',back_populates='specialite_departement')
    specialite_etudiant=relationship('Etudiant',back_populates='etudiant_specialite')

class Etudiant(Base):
    __tablename__ = 'Etudiant'
    idEtudiant = Column(Integer, primary_key=True)
    nomEtudiant = Column(String(50))
    prenomEtudiant = Column(String(50))
    idProfesseur = Column(Integer, ForeignKey('Professeur.idProfesseur'))
    idSpecialite = Column(Integer, ForeignKey('Specialite.idSpecialite'))
    etudiant_specialite=relationship('Specialite',back_populates='specialite_etudiant')
    professeur_conseiller=relationship('Professeur',back_populates='etudiant_conseiller')
    classes=relationship('Classe',secondary='Sinscrire',back_populates='etudiants')





Base.metadata.create_all(engine)

#insertion des données
#insertion dans contrat
contrat1 = Contrat(typeContrat='CDI')
contrat2 = Contrat(typeContrat='CDD')
contrat3 = Contrat(typeContrat='Recherche')
session.add_all([contrat1, contrat2, contrat3])

# insertion dans Batiment
batiment1 = Batiment(nomBatiment='Batiment A')
batiment2 = Batiment(nomBatiment='Batiment B')
session.add_all([batiment1, batiment2])
session.commit()

#insertion dans professeurs
professeur1 = Professeur(nomProfesseur='Jean Dupont', Id_Contrat=1)
professeur2 = Professeur(nomProfesseur='Paul', Id_Contrat=2)
professeur3 = Professeur(nomProfesseur='Patrick Martineau', Id_Contrat=2)
professeur4 = Professeur(nomProfesseur='Emmanuel Neron', Id_Contrat=1)
professeur5 = Professeur(nomProfesseur='Alexandre Neron', Id_Contrat=1)
session.add_all([professeur1, professeur2,professeur3,professeur4,professeur5])
session.commit()

cours1 = Cours(nomCours='Microeconomie', idProfesseur=professeur1.idProfesseur)
cours2 = Cours(nomCours='Gestion de la Production', idProfesseur=professeur2.idProfesseur)
cours3 = Cours(nomCours='Programmation C', idProfesseur=professeur2.idProfesseur)
cours4 = Cours(nomCours='Interface Homme Machine', idProfesseur=professeur2.idProfesseur)
cours5 = Cours(nomCours='Rapport Societal', idProfesseur=professeur2.idProfesseur)
session.add_all([cours1, cours2,cours3,cours4,cours5])
session.commit()

#insertion dans salle
salle1 = Salle(codeSalle='Salle A', idBatiment=batiment1.idBatiment)
salle2 = Salle(codeSalle='Salle B', idBatiment=batiment2.idBatiment)
session.add_all([salle1, salle2])
session.commit()

classe1=Classe(nomClasse='Principes Fondamentaux de Gestion',nombrePlace=22,dateClasse='2024-05-01',heureDebut='12:12:00',heureFin='11:10:00',idSalle=salle1.idSalle,idCours=cours2.idCours)
classe2=Classe(nomClasse='windows B',nombrePlace=20,dateClasse='2024-07-01',heureDebut='12:12:00',heureFin='11:10:00',idSalle=salle2.idSalle,idCours=cours2.idCours)
session.add_all([classe1,classe2])
session.commit()

faculte1 = Faculte(nomFaculte='Faculte de medecine',idProfesseur=professeur3.idProfesseur)
faculte2 = Faculte(nomFaculte='Faculte des sciences appliquées',idProfesseur=professeur1.idProfesseur)
faculte3 = Faculte(nomFaculte='Faculte des sciences de gestion',idProfesseur=professeur3.idProfesseur)
faculte4 = Faculte(nomFaculte='Economie',idProfesseur=professeur1.idProfesseur)
session.add_all([faculte1, faculte2,faculte3,faculte4])
session.commit()

departement1 = Departement(nomDepartement='Informatique', idFaculte=faculte2.idFaculte,idProfesseur=professeur1.idProfesseur)
departement2 = Departement(nomDepartement='Gestion', idFaculte=faculte3.idFaculte,idProfesseur=professeur2.idProfesseur)
session.add_all([departement1, departement2])
session.commit()

specialite1 = Specialite(nomSpecialite='Methodes Informatique', idDepartement=departement1.idDepartement)
specialite2 = Specialite(nomSpecialite='Gestion', idDepartement=departement2.idDepartement)
session.add_all([specialite1, specialite2])
session.commit()

etudiant1=Etudiant(nomEtudiant='michel',prenomEtudiant='nkouba',idProfesseur=professeur1.idProfesseur,idSpecialite=specialite1.idSpecialite)
etudiant2=Etudiant(nomEtudiant='ulrich',prenomEtudiant='marius',idProfesseur=professeur1.idProfesseur,idSpecialite=specialite1.idSpecialite)
etudiant3=Etudiant(nomEtudiant='clotilde',prenomEtudiant='nkouba',idProfesseur=professeur2.idProfesseur,idSpecialite=specialite2.idSpecialite)
session.add_all([etudiant1,etudiant2,etudiant3])

session.commit()

sinscrire1=Sinscrire(idEtudiant=etudiant1.idEtudiant,idClasse=classe1.idClasse,note=18)
sinscrire2=Sinscrire(idEtudiant=etudiant2.idEtudiant,idClasse=classe1.idClasse,note=16)
sinscrire3=Sinscrire(idEtudiant=etudiant3.idEtudiant,idClasse=classe1.idClasse,note=10)
sinscrire4=Sinscrire(idEtudiant=etudiant1.idEtudiant,idClasse=classe2.idClasse,note=15)
session.add_all([sinscrire1,sinscrire2,sinscrire3,sinscrire4])

session.commit()

enseigner1=Enseigner(idProfesseur=professeur1.idProfesseur,idDepartement=departement1.idDepartement)
enseigner2=Enseigner(idProfesseur=professeur2.idProfesseur,idDepartement=departement1.idDepartement)
enseigner3=Enseigner(idProfesseur=professeur3.idProfesseur,idDepartement=departement1.idDepartement)
session.add_all([enseigner1,enseigner2,enseigner3])
session.commit()
"""req1
query = session.query(Professeur.nomProfesseur, Etudiant.nomEtudiant)\
               .join(Faculte, Faculte.idFaculte == Professeur.idFaculte)\
               .join(Etudiant, Professeur.idProfesseur == Etudiant.idProfesseur)\
               .filter(Faculte.nomFaculte == 'Économie')

# Exécution de la requête
results = query.all()

# Affichage des résultats
for result in results:
    print(result)"""

"""req2
query = session.query(Salle.codeSalle, Etudiant.nomEtudiant)\
               .join(Classe, Classe.idSalle == Salle.idSalle)\
               .join(Cours, Cours.idCours == Classe.idCours)\
               .join(Sinscrire, Sinscrire.idClasse == Classe.idClasse)\
               .join(Etudiant, Etudiant.idEtudiant == Sinscrire.idEtudiant)\
               .filter(Classe.nomClasse == 'Principes Fondamentaux de Gestion')\
               .filter(Cours.nomCours == 'Gestion de la Production')

# Exécution de la requête
results = query.all()

# Affichage des résultats
for result in results:
    print(result)"""

"""req3
query = session.query(Professeur.nomProfesseur)\
               .join(Enseigner, Professeur.idProfesseur == Enseigner.idProfesseur)\
               .join(Departement, Departement.idDepartement == Enseigner.idDepartement)\
               .join(Faculte, Faculte.idFaculte == Departement.idFaculte)\
               .filter(Departement.nomDepartement == 'Informatique')\
               .filter(Faculte.nomFaculte == 'Faculté des Sciences Appliquées')

# Exécution de la requête
results = query.all()

# Affichage des résultats
for result in results:
    print(result)"""

"""req4
query = session.query(Sinscrire.note, Classe.nomClasse)\
               .join(Etudiant, Etudiant.idEtudiant == Sinscrire.idEtudiant)\
               .join(Classe, Classe.idClasse == Sinscrire.idClasse)\
               .filter(Etudiant.nomEtudiant == 'Michel')

# Exécution de la requête
results = query.all()

# Affichage des résultats
for result in results:
    print(result)"""

session.close()