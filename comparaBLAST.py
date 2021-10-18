#python comparaBLAST.py -a Fh_com_filtro_30_bats.txt -b Fh_com_filtro_30_vir.txt -o Fh_comparado.tab
#python comparaBLAST.py -a La_com_filtro_30_bats.txt -b La_com_filtro_30_vir.txt -o La_comparado.tab
#python comparaBLAST.py -a Nm_com_filtro_30_bats.txt -b Nm_com_filtro_30_vir.txt -o Nm_comparado.tab
import argparse
import csv

ajuda = 'comparaBLAST.py -a <arquivo tabular contra banco A> -b <arquivo tabular contra banco B> -o <arquivo de output> \n'
ajuda = ajuda + '\nParametros obrigatorios\n'
ajuda = ajuda + '-a\tArquivo de entrada tabular contra banco A\n'
ajuda = ajuda + '-b\tArquivo de entrada contra banco B\n'
ajuda = ajuda + '-o\tArquivo de saida\n'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-a')
parser.add_argument('-b')
parser.add_argument('-o')
parser.add_argument('-h', '--help', action='store_true')
args = parser.parse_args()

def ordenar(arquivo):
    seqs = dict()
    for linha in arquivo.readlines():
        colunas = linha.split('\t')
        qseqid = colunas[0]
        bitscore = float(colunas[4])
        evalue = float(colunas[6])
        if qseqid in seqs.keys():
            item = seqs[qseqid]
            if evalue < item[0]:
                seqs[qseqid] = evalue
            elif (not evalue > item[0]) and (bitscore > item[1]):
                seqs[qseqid] = [evalue, bitscore]
        if not qseqid in seqs.keys():
            seqs[qseqid] = [evalue, bitscore]
    return seqs


def comparar(A, B):
    AB = dict()
    seqs = list(A.keys()) + list(B.keys())
    for qseqid in seqs:
        if qseqid in A.keys() and qseqid in B.keys():
            x = A[qseqid]
            y = B[qseqid]
            if x[0] < y[0]:
                AB[qseqid] = [x[0], y[0], 'A']
            elif x[0] > y[0]:
                AB[qseqid] = [x[0], y[0], 'B']
            elif x[1] > y[1]:
                AB[qseqid] = [x[0], y[0], 'A']
            elif x[1] < y[1]:
                AB[qseqid] = [x[0], y[0], 'B']
    return AB


if args.help == True:
    print(ajuda)
elif args.a == None or args.b == None:
    print('ERRO: Arquivo de entrada ausente\n')
    print(ajuda)
elif args.o == None:
    print('ERRO: Arquivo de saida ausente\n')
    print(ajuda)
else:
    A = ordenar(open(args.a, 'r'))
    B = ordenar(open(args.b, 'r'))
    AB = comparar(A, B)
    saida = open(args.o, mode='w')
    escritor = csv.writer(saida,
                          delimiter='\t',
                          quotechar='"',
                          quoting=csv.QUOTE_MINIMAL)
    escritor.writerow([
        'A_qseqid', 'A_evalue', 'B_qseqid', 'B_evalue', 'AB_qseqid',
        'A_evalue', 'B_evalue', 'Escolha'
    ])
    for i in range(max(len(A), len(B), len(AB))):
        linha = []
        if i < len(A):
            linha.append(list(A.keys())[i])
            linha.append(list(A[linha[0]])[0])
        else:
            linha.extend(['', ''])
        if i < len(B):
            linha.append(list(B.keys())[i])
            linha.append(list(B[linha[2]])[0])
        else:
            linha.extend(['', ''])
        if i < len(AB):
            linha.append(list(AB.keys())[i])
            linha.extend(AB[linha[4]])
        else:
            linha.extend(['', '', '', ''])
        escritor.writerow(linha)
    saida.close()
