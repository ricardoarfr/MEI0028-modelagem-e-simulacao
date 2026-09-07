"""nystroem_sgd.py — SVM linear escalável sobre aproximação de Nyström do núcleo RBF, treinado por gradiente
estocástico (perda hinge) em LOTES: a matriz de atributos transformados nunca é materializada por inteiro
(memória ≈ tamanho do lote × D). Substitui LinearSVC/liblinear, cuja representação esparsa de Φ densa exige
~16 bytes por elemento (D=1000 em 1,05 M linhas → > 8 GB). Implementações: scikit-learn (PEDREGOSA et al., 2011)."""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import SGDClassifier
class NystroemSGD(BaseEstimator, ClassifierMixin):
    def __init__(self, n_components=500, alpha=1e-4, epochs=5, chunk=100_000, gamma=None, random_state=0, n_jobs=4):
        self.n_components=n_components; self.alpha=alpha; self.epochs=epochs; self.chunk=chunk; self.gamma=gamma; self.random_state=random_state; self.n_jobs=n_jobs
    def fit(self, X, y):
        X=np.asarray(X,dtype=np.float32); y=np.asarray(y); rng=np.random.RandomState(self.random_state)
        self.classes_=np.unique(y)
        self.nys_=Nystroem(kernel="rbf",gamma=self.gamma,n_components=self.n_components,random_state=self.random_state,n_jobs=self.n_jobs).fit(X)
        self.sgd_=SGDClassifier(loss="hinge",alpha=self.alpha,learning_rate="optimal",average=True,random_state=self.random_state,n_jobs=self.n_jobs,max_iter=1,tol=None)
        n=len(y)
        for ep in range(self.epochs):
            idx=rng.permutation(n)
            for s in range(0,n,self.chunk):
                b=idx[s:s+self.chunk]; Phi=self.nys_.transform(X[b]).astype(np.float32)
                self.sgd_.partial_fit(Phi,y[b],classes=self.classes_)
        return self
    def decision_function(self, X):
        X=np.asarray(X,dtype=np.float32); out=[]
        for s in range(0,len(X),self.chunk): out.append(self.sgd_.decision_function(self.nys_.transform(X[s:s+self.chunk]).astype(np.float32)))
        return np.vstack(out)
    def predict(self, X):
        X=np.asarray(X,dtype=np.float32); out=[]
        for s in range(0,len(X),self.chunk): out.append(self.sgd_.predict(self.nys_.transform(X[s:s+self.chunk]).astype(np.float32)))
        return np.concatenate(out)
