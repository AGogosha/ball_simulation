import os

fn main () {
	numbers:=[1,2,3,4,5,6,7,8,9,10]
	mut threads:=[]thread {cap:numbers.len}
	for i in 0..numbers.len{
		threads << spawn logged_fn(fn [numbers, i] () ! { expensive_calculation(numbers, i)! })
	}
	threads.wait()
}

fn expensive_calculation(data []int, iterator int) ! {
	mut f := os.create('example_{$iterator}.csv')!
	f.writeln('x,y')!
	for number in data {
		y:=number*2
		f.writeln('$number,$y')!
	}
	f.close()
}

fn logged_fn( f fn() ! ) {
      f() or { eprintln(err) return }
}