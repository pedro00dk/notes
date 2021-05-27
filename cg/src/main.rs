mod util;

use std::iter::FromIterator;
use util::Vx;

fn main() {
    let v = util::V3 { x: 0.0, y: 2.0, z: 0.0 };
    // let u = util::V3::<f32>::of(0.0f32);
    let mut u = util::V3::<f32>::default() + 2.0 + v;
    u += 3.0;
    u += v;

    let x = vec![1f32, 2.0, 3.0, 4.0, 5.0];
    let z = util::V3::from_iter(x);
    let u = z.into_iter();
    let mut b = z + z;
    b += v;
    // let c: [i32; 3] = From::from(b);
    let j = &b[0..1];
    println!("{}", b == v);
    println!("{}", b[0]);
    println!("{}", b[1]);
    println!("{}", b[2]);
    b[2] = 3.0;
    // &b[0..2] = 3.0;
    println!("{}", b[2]);
    // println!("{:?}", &b[0..=3]);
    println!("{:?}", b);

    println!("Hello, world! ${:?}  ---- {:?} {:?}", z, u, b);
}
