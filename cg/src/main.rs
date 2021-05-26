mod util;

use std::iter::FromIterator;
use util::Vx;

fn main() {
    let v = util::V3 { x: 0.0, y: 2.0, z: 0.0 };
    // let u = util::V3::<f32>::of(0.0f32);
    let mut u = util::V3::<f32>::default() + 2.0 + v;
    u += 3.0;
    u += v;

    let x = vec![1, 2, 3, 4, 5];
    let z = util::V3::from_iter(x);
    let u = z.into_iter();
    let b = z + z;

    println!("Hello, world! ${:?}  ---- {:?} {:?}", z, u, b);
}
