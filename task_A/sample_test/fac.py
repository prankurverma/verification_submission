def fac(n):
    if n>1:
        return n*fac(n-1)
    if n==1 or n==0:
        return 1

def main():
    n = int(input())
    print(fac(n))

if __name__ == "__main__":
    main()