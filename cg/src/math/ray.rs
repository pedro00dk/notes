use crate::math;

pub struct Ray {
    pub origin: math::VR<f32, 4>,
    pub direction: math::VR<f32, 4>,
}

impl Ray {
    pub fn at(&self, t: f32) -> math::VR<f32, 4> {
        self.origin + self.direction * t
    }
}
