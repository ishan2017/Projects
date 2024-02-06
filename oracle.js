function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
  }

function generateInput(n){  
  let output = [];
  for(let i = 0; i < n; ++i){
    let x = [];
    for(let j = 0; j < n; ++j){
      let y = randomInt(0, n);
      while(x.includes(y)){
        y = randomInt(0, n);
      }
      x.push(y);
    }
    output.push(x);
  }
  return output;
}

function oracle(f) {
  let numTests = 200;
  for (let i = 0; i < numTests; ++i) {
    let n = randomInt(3, 50);
    let companies = generateInput(n);
    let candidates = generateInput(n);
    let hires = f(companies, candidates);
    test('Hires length is correct', function() {
    assert(companies.length === hires.length);
    });
    test('Hires contains no duplicates', function() {
    assert(noDuplicates(hires));
    });
    test('All elements in Hires are contained within 0 and n-1', function() {
    assert(hires.reduce(contained, {x: true, y: n}).x === true);
    });
    test('Hires follows stable matching', function() {
    for (let j = 0; j < hires.length; ++j){
      let company = hires[j].company;
      let candidate = hires[j].candidate;
      assert(isStablePair(company, candidate, companies, candidates, hires));
    }
    });
  }
}

function noDuplicates(array){
  let uniqueCompanyIntegers = [];
  let compNoDupe = true;
  let uniqueCandidateIntegers = [];
  let candNoDupe = true;
  for (let i = 0; i < array.length; ++i){
    let x = array[i].company;
    let y = array[i].candidate;
    if (uniqueCompanyIntegers.includes(x)){
      compNoDupe = false;
      break;
    }
    if (uniqueCandidateIntegers.includes(y)){
      candNoDupe = false;
      break;
    }
    uniqueCompanyIntegers.push(x);
    uniqueCandidateIntegers.push(y);
  }
  if (compNoDupe === true && candNoDupe === true){
    return true;
  }
  else{
    return false;
  }
}

function contained(acc, next){
  if (acc.x === false){
    return acc;
  }
  if (next.candidate >= 0 && next.candidate < acc.y  && next.company >= 0 && next.company < acc.y){
    return acc;
  }
  else{
    return {x: false, y:acc.y};
  }
}

function isStablePair(company, candidate, compOrder, canOrder, hires){
  let result = true;
  let preferedCandidates = compOrder[company].reduce(subSet, {x: [], y: candidate, z: false}).x;
  if (preferedCandidates.length === 0){
    return true;
  }
  for (let i = 0; i < preferedCandidates.length; ++i){
    let candidateMatch = 0;
    for (let j = 0; j < hires.length; ++j){
      if (hires[j].candidate === preferedCandidates[i]){
        candidateMatch = hires[j].company;
        break;
      }
    }
    let preferedCompanies = canOrder[preferedCandidates[i]].reduce(subSet, {x: [], y: candidateMatch, z: false}).x;
    if (preferedCompanies.includes(company)){
      result = false;
      break;
    }
  }
  return result;
}

function subSet(acc, next){
  if (acc.z === true){
    return acc;
  }
  if (acc.y === next){
    acc.z = true;
    return acc;
  }
  else{
    acc.x.push(next);
    return acc;
  }
}

test('generateInput function', function() {
  //check that generateInput with an argument of 0 will return an empty array
  const x = generateInput(0);
  assert(x.length === 0);
  //check that array generateInput returns and the arrays contained within it are of the correct length
  const y = generateInput(5);
  assert(y.length === 5);
  for (let i = 0; i < y.length; ++i){
    assert(y[i].length === 5);
  }
  //check that none of the permutations within the returned array contains duplicates
  const z = generateInput(7);
  let result = true;
  for (let j = 0; j < z.length; ++j){
    if (result === false){
      break;
    }
    let uniqueIntegers = [];
    for (let k = 0; k < z[j].length; ++k){
      if (uniqueIntegers.includes(z[j][k])){
        result = false;
        break;
      }
      uniqueIntegers.push(z[j][k]);
    }
  }
  assert(result === true);
});

test('noDuplicates function', function() {
  //noDuplicates should return true on empty array
  assert(noDuplicates([]) === true);
  const x = [{company: 0, candidate: 0}, {company: 1, candidate: 1}, {company: 2, candidate: 2}];
  const y = [{company: 0, candidate: 0}, {company: 1, candidate: 1}, {company: 0, candidate: 2}];
  const z = [{company: 0, candidate: 0}, {company: 1, candidate: 1}, {company: 2, candidate: 0}];
  const a = [{company: 0, candidate: 0}, {company: 1, candidate: 1}, {company: 0, candidate: 0}];
  //noDuplicates should return true when neither the company or candidate attributes have a duplicate
  assert(noDuplicates(x) === true);
  //noDuplicates should return false when the company attribute has a duplicate
  assert(noDuplicates(y) === false);
  //noDuplicates should return false when the candidate attribute has a duplicate
  assert(noDuplicates(z) === false);
  //noDuplicates should return false when both attributse have a duplicate
  assert(noDuplicates(a) === false);
});

test('contained function works properly with reduce', function() {
  const x = [{company: 0, candidate: 0}, {company: 1, candidate: 1}, {company: 2, candidate: 2}, {company: 3, candidate: 3}];
  //The mock hires array x has four elements so the initial object passed into the reduce function should be {x: true, y:4} (where 4 would be n)
  //Since all company and candidate values in x are between 0 and n-1 (0 and 3), the x attribute of the returned object should equal true
  let result = x.reduce(contained, {x: true, y: 4});
  assert(result.x === true);
  const y = [{company: 0, candidate: 0}, {company: 1, candidate: 1}, {company: 2, candidate: 2}, {company: 4, candidate: 3}];
  //One of the company attributes in y has a value of 4, meaning the x attribute of the object returned should equal false
  let result2 = y.reduce(contained, {x: true, y: 4});
  assert(result2.x === false);
});

test('subSet function works properly with reduce', function() {
  /**
  When used with the reduce function, subSet should return an object with an x attribute that is an array
  containing all elements of the array before the first element that is equal to the y attribute of the object
  **/
  const x = [4, 2, 5, 9, 1, 6, 12, 3];
  let result = x.reduce(subSet, {x: [], y: 4, z: false});
  //since the y element of the object is 4, and the first element of x is 4, the x attribute of result should be an empty array
  assert(result.x.length === 0);
  let result2 = x.reduce(subSet, {x: [], y: 12, z: false});
  const y = [4, 2, 5, 9, 1, 6];
  //The x attribute of result2 should be equal to the array y since it contains all elements of x leading up to 12
  assert(y.length === result2.x.length);
  for (let i = 0; i < y.length; ++i){
    assert(y[i] === result2.x[i]);
  }
});
