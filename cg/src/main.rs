mod util;

use util::Vx;

fn main() {
    let v = util::V3 { x: 0.0, y: 2.0, z: 0.0 };
    // let u = util::V3::<f32>::of(0.0f32);
    let mut u = util::V3::<f32>::default() + 2.0 + v;
    u += 3.0;
    u += v;

    println!("Hello, world! {:?} {:?} {:?}", -v, u - 3.0, v + u);
}
