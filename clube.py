#!/usr/bin/env python
# coding: utf-8

PEDANTE = False

class Pessoa():
  def __init__(self, nome, wiki=None):
    self.nome = nome
    self.wiki = wiki
    self.cmc = None
    self.associacao = []
    self.padawans = []

  def __repr__(self):
    return self.nome

  def apresenta_padawans(self, pessoas):
    for p in pessoas:
      self.apresenta_padawan(p)

  def apresenta_padawan(self, pessoa):
    pessoa.apresentacao = self.cmc.dia
    self.padawans.append(pessoa)
    self.cmc.padawans.append(pessoa)

class ConselhoMandaChuva():
  def __init__(self, fundadores=[]):
    self.num_fundadores = len(fundadores)
    self.associados = fundadores
    self.padawans = []
    self.ex_associados = []

    for f in fundadores:
      f.cmc = self

  def pergunta(self, p):
    print("Pergunta: '{}'".format(p))

  def data(self, d):
    self.dia = d
    print("CMC de {}:".format(d))

  def readmite_associado(self, pessoa):
    pessoa.cmc = self

    if pessoa in self.ex_associados:
      self.ex_associados.remove(pessoa)

    if pessoa not in self.associados:
      self.associados.append(pessoa)

    pessoa.associacao.append([self.dia, None])

  def aprova_associado(self, pessoa, endosso=None, fundador=False):
    pessoa.cmc = self
    pessoa.associacao.append([self.dia, None])

    if pessoa in self.padawans:
      self.padawans.remove(pessoa)
    else:
      if not fundador and endosso != "HACK":
        print("ERRO: Aprovando associado '{}' que não é padawan de ninguém!".format(pessoa.nome))
    if pessoa not in self.associados:
      self.associados.append(pessoa)

  def observa_desligamento(self, pessoa, motivo=None):
    pessoa.cmc = None

    if pessoa not in self.ex_associados:
      self.ex_associados.append(pessoa)

    if pessoa in self.associados:
      self.associados.remove(pessoa)
      try:
        pessoa.associacao[-1][1] = self.dia
      except:
        if PEDANTE:
          print("ERRO: nao achei registro de associacao para '{}'".format(pessoa.nome))
    else:
      print("ERRO: Desligando '{}' que nem era associado!".format(pessoa.nome))

  def print_padawans(self):
    print("Padawans órfãos:\n\t{}".format('\n\t'.join(map(lambda x: "{}: {}".format(x.apresentacao, x.nome), self.padawans))))

  def print_associados(self):
    print("Associados:\n\t{}".format('\n\t'.join(map(lambda x: "{} ({})".format(x.nome, len(x.padawans)), self.associados))))

  def output_graph(self):
    pessoas = self.associados + self.padawans + self.ex_associados
    fundadores = "fundadores [label=\"Sócios Fundadores do Garoa Hacker Clube\"];\n\n"
    fundadores += "\n".join(["fundadores -> Pessoa_{};".format(n) for n in range(self.num_fundadores)])

    padawans = "\n#padawans\n"
    for p in pessoas:
      for padawan in p.padawans:
        padawans += "Pessoa_{} -> Pessoa_{};\n".format(pessoas.index(p),
                                                       pessoas.index(padawan))

    pessoas_str = "\n#pessoas\n"
    for p in pessoas:
      pessoas_str += "Pessoa_{} [label=\"{}\"];\n".format(pessoas.index(p),
                                                          '\n'.join(p.nome.split(" ")))

    output = """\
digraph G {
  node [shape=egg,
        labelloc=c,
        fontsize=5,
        style=filled,
        fontcolor="#eeffee"
        color="#559955"];
""" + str(fundadores) + "\n" + str(padawans) + "\n" + str(pessoas_str) + "\n}"

    open("garoa-associados.gv", "w").write(output)
