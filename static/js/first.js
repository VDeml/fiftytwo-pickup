let maCIsla = [3,5,10,4,2,1,16,7];

let soucet = 0;

soucet = maCIsla.filter(function(x) {
    return x % 2 === 0;
}).reduce(function(cislo1, cislo2) {
    return cislo1 + cislo2;
});


console.log(soucet);