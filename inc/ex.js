const books = [
    { title: 'Eloquent JavaScript', price: 29.99 },
    { title: 'JavaScript: The Good Parts', price: 19.99 }
  ];
const titleColumnWidth = 30;
const priceColumnWidth = 10;
books.forEach(b => {
  let title = b.title.padEnd(titleColumnWidth, ' ');
  let price = b.price.toString().padStart(priceColumnWidth, ' ');
  console.log(`| ${title} | ${price} |`)
  console.log(''.padStart(titleColumnWidth + priceColumnWidth + 7,'-'))
})  
////

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{([0-9]+)}/g, function (match, index) {
      return typeof args[index] == 'undefined' ? match : args[index];
    });
};
// console.log('Hello {0}, your order {1} has been shipped.'.format('John', 10001));
